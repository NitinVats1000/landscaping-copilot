"""Pydantic schemas — the API contract. Deliberately separate from the DB models."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """What the client SENDS to create a project."""

    title: str = Field(min_length=1, max_length=200)
    scene_type: str | None = Field(default=None, max_length=50)


class ProjectRead(BaseModel):
    """What the API RETURNS. from_attributes lets it read an ORM object directly."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    scene_type: str | None
    status: str
    created_at: datetime
