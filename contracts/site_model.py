"""
SiteModel — the data contract at the spine of the AI Landscaping Copilot.

Every stage reads from and writes to this object:

    vision pipeline ──writes──▶ SiteModel ──reads──▶ agents ──reads──▶ report

If a v1 feature has no field here, it is not really designed yet. This file is the
single source of truth that lets ~6 services agree on shapes without reading each
other's internals (loose coupling via contract).

Design principles encoded below (each is an interview talking point):
  1. Optional + confidence EVERYWHERE — the pipeline is allowed to be honestly unsure.
  2. Units live in field names (area_m2, sun_hours_*) — the Mars Climate Orbiter rule.
  3. Controlled vocab as Enums — "kind" can't drift into 12 spellings over time.
  4. schema_version — this WILL evolve; make future migrations explicit, not silent.
  5. Validate at the boundary (extra='forbid', validators) — garbage can't enter quietly.
  6. Store geometry resolution-independently (normalized [0..1] coords).
"""

from __future__ import annotations

from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class SunClass(str, Enum):
    full_sun = "full_sun"   # >= 6 direct-sun hours (summer)
    part_sun = "part_sun"   # 3–6 hours
    shade = "shade"         # < 3 hours


class RegionKind(str, Enum):
    empty_bed = "empty_bed"          # plantable target
    existing_plant = "existing_plant"
    lawn = "lawn"
    paving = "paving"
    water = "water"
    structure = "structure"          # wall, fence, building
    other = "other"


class CameraIntrinsics(BaseModel):
    """What we know about the camera. Drives metric-depth calibration in Phase 4."""

    focal_length_mm: float | None = None
    sensor_width_mm: float | None = None
    image_width_px: int
    image_height_px: int
    # provenance matters: an AR-measured scale is trustworthy; an EXIF guess less so
    source: str = "unknown"  # "exif" | "ar_session" | "estimated" | "unknown"


class SiteRegion(BaseModel):
    """One spatially distinct area of the photo (a bed, the lawn, a paved path...)."""

    model_config = ConfigDict(use_enum_values=True)

    kind: RegionKind
    # polygon in NORMALIZED image coords [0..1] → independent of image resolution
    polygon_norm: list[tuple[float, float]] = Field(default_factory=list)

    area_m2: float | None = None             # None until depth calibration lands
    material: str | None = None              # "soil" | "grass" | "gravel" | ...
    sun_hours_summer: float | None = None
    sun_class: SunClass | None = None

    mask_s3_key: str | None = None           # where the raw mask is stored
    detected_species: str | None = None      # scientific name, if existing_plant
    detection_confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    @field_validator("area_m2")
    @classmethod
    def _area_non_negative(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("area_m2 cannot be negative")
        return v


class SiteModel(BaseModel):
    """The complete structured understanding of one site, produced by the vision pipeline."""

    # extra='forbid' → a typo'd field name (e.g. 'plantible_area_m2') RAISES instead of
    # silently being ignored. This single line catches a whole class of integration bugs.
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    project_id: str
    schema_version: str = "0.1.0"

    indoor: bool
    scene_type: str                                    # "home_garden" for v1
    scene_confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    intrinsics: CameraIntrinsics | None = None
    total_area_m2: float | None = None
    plantable_area_m2: float | None = None

    regions: list[SiteRegion] = Field(default_factory=list)
    aesthetic_features: dict = Field(default_factory=dict)  # palette, openness, etc.

    # the pipeline writes here whenever it had to guess — surfaced to the user as caveats
    confidence_notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _plantable_within_total(self) -> "SiteModel":
        if (
            self.plantable_area_m2 is not None
            and self.total_area_m2 is not None
            and self.plantable_area_m2 > self.total_area_m2 + 1e-6
        ):
            raise ValueError("plantable_area_m2 cannot exceed total_area_m2")
        return self

    @property
    def empty_beds(self) -> list[SiteRegion]:
        """Convenience the agents will reach for constantly."""
        return [r for r in self.regions if r.kind == RegionKind.empty_bed.value]
