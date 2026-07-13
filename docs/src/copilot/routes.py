"""Project API endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from copilot.db import get_session
from copilot.models import Project
from copilot.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/v1/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    session: AsyncSession = Depends(get_session),
) -> Project:
    """Create a project. 201 = a new resource was created."""
    project = Project(title=payload.title, scene_type=payload.scene_type)
    session.add(project)
    await session.commit()
    await session.refresh(project)  # reload DB-generated fields (id, created_at)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    session: AsyncSession = Depends(get_session),
) -> list[Project]:
    """List all projects, newest first."""
    result = await session.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Project:
    """Fetch one project by id. 404 if it doesn't exist."""
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return project
