"""
Tests for the SiteModel contract.

Even in a 'design' phase we test the contract, because the contract IS code that the
whole system depends on. Run from docs/contracts/:  pytest test_site_model.py -v
"""

import pytest

from site_model import (
    CameraIntrinsics,
    RegionKind,
    SiteModel,
    SiteRegion,
    SunClass,
)


def test_valid_model_builds():
    sm = SiteModel(
        project_id="demo-1",
        indoor=False,
        scene_type="home_garden",
        scene_confidence=0.9,
        intrinsics=CameraIntrinsics(
            image_width_px=4032, image_height_px=3024, source="exif"
        ),
        total_area_m2=20.0,
        plantable_area_m2=6.5,
        regions=[
            SiteRegion(
                kind=RegionKind.empty_bed,
                area_m2=4.0,
                material="soil",
                sun_hours_summer=6.5,
                sun_class=SunClass.full_sun,
            ),
            SiteRegion(
                kind=RegionKind.existing_plant,
                detected_species="Rosa chinensis",
                detection_confidence=0.82,
            ),
        ],
        confidence_notes=["depth calibration used a door-height prior"],
    )
    assert sm.plantable_area_m2 <= sm.total_area_m2
    # use_enum_values=True means enums serialize to their string value
    assert sm.regions[0].sun_class == "full_sun"
    # the convenience property works
    assert len(sm.empty_beds) == 1


def test_plantable_exceeding_total_is_rejected():
    with pytest.raises(Exception):
        SiteModel(
            project_id="x",
            indoor=False,
            scene_type="home_garden",
            total_area_m2=5.0,
            plantable_area_m2=9.0,  # invariant violation
        )


def test_unknown_field_is_rejected():
    # extra='forbid' catches typos at the boundary instead of silently dropping them
    with pytest.raises(Exception):
        SiteModel(
            project_id="x",
            indoor=False,
            scene_type="home_garden",
            plantible_area_m2=3.0,  # deliberate typo
        )


def test_confidence_must_be_a_probability():
    with pytest.raises(Exception):
        SiteRegion(kind=RegionKind.existing_plant, detection_confidence=1.4)


def test_json_round_trip_is_stable():
    sm = SiteModel(project_id="rt", indoor=False, scene_type="home_garden")
    restored = SiteModel.model_validate_json(sm.model_dump_json())
    assert restored == sm
