from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.models.milestone import (
    MilestoneCreate,
    MilestoneResponse,
    MilestoneUpdate,
)
from app.supabase import supabase


router = APIRouter(
    prefix="/milestones",
    tags=["Milestones"],
)


@router.post("", response_model=MilestoneResponse)
def create_milestone(payload: MilestoneCreate):
    response = (
        supabase
        .table("milestones")
        .insert(payload.model_dump(mode="json"))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to create milestone",
        )

    return response.data[0]


@router.get("", response_model=list[MilestoneResponse])
def list_milestones(
    mission_id: UUID = Query(...),
):
    response = (
        supabase
        .table("milestones")
        .select("*")
        .eq("mission_id", str(mission_id))
        .order("order_index")
        .execute()
    )

    return response.data


@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_milestone(milestone_id: UUID):
    response = (
        supabase
        .table("milestones")
        .select("*")
        .eq("id", str(milestone_id))
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Milestone not found",
        )

    return response.data


@router.patch("/{milestone_id}", response_model=MilestoneResponse)
def update_milestone(
    milestone_id: UUID,
    payload: MilestoneUpdate,
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
        .table("milestones")
        .update(updates)
        .eq("id", str(milestone_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Milestone not found",
        )

    return response.data[0]


@router.delete("/{milestone_id}")
def delete_milestone(milestone_id: UUID):
    response = (
        supabase
        .table("milestones")
        .delete()
        .eq("id", str(milestone_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Milestone not found",
        )

    return {
        "message": "Milestone deleted",
        "id": str(milestone_id),
    }
