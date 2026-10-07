from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.models.mission import (
    MissionCreate,
    MissionResponse,
    MissionUpdate,
)
from app.supabase import supabase


router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)


@router.post(
    "",
    response_model=MissionResponse,
)
def create_mission(payload: MissionCreate):
    response = (
        supabase
        .table("missions")
        .insert(payload.model_dump(mode="json"))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to create mission",
        )

    return response.data[0]


@router.get(
    "",
    response_model=list[MissionResponse],
)
def list_missions(
    user_id: UUID = Query(...),
):
    response = (
        supabase
        .table("missions")
        .select("*")
        .eq("user_id", str(user_id))
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


@router.get(
    "/{mission_id}",
    response_model=MissionResponse,
)
def get_mission(mission_id: UUID):
    response = (
        supabase
        .table("missions")
        .select("*")
        .eq("id", str(mission_id))
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Mission not found",
        )

    return response.data


@router.patch(
    "/{mission_id}",
    response_model=MissionResponse,
)
def update_mission(
    mission_id: UUID,
    payload: MissionUpdate,
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
        .table("missions")
        .update(updates)
        .eq("id", str(mission_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Mission not found",
        )

    return response.data[0]


@router.delete("/{mission_id}")
def delete_mission(mission_id: UUID):
    response = (
        supabase
        .table("missions")
        .delete()
        .eq("id", str(mission_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Mission not found",
        )

    return {
        "message": "Mission deleted",
        "id": str(mission_id),
    }
