from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.models.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.supabase import supabase


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("", response_model=ProjectResponse)
def create_project(payload: ProjectCreate):
    response = (
        supabase
        .table("projects")
        .insert(payload.model_dump(mode="json"))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to create project",
        )

    return response.data[0]


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    mission_id: UUID = Query(...),
):
    response = (
        supabase
        .table("projects")
        .select("*")
        .eq("mission_id", str(mission_id))
        .order("priority", desc=True)
        .execute()
    )

    return response.data


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID):
    response = (
        supabase
        .table("projects")
        .select("*")
        .eq("id", str(project_id))
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return response.data


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
):
    updates = payload.model_dump(
        mode="json",
        exclude_unset=True,
    )

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields to update",
        )

    response = (
        supabase
        .table("projects")
        .update(updates)
        .eq("id", str(project_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return response.data[0]


@router.delete("/{project_id}")
def delete_project(project_id: UUID):
    response = (
        supabase
        .table("projects")
        .delete()
        .eq("id", str(project_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {
        "message": "Project deleted",
        "id": str(project_id),
    }
