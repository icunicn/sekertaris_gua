from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime, timezone

from app.models.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TodayProgressResponse,
)
from app.supabase import supabase


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    response = (
        supabase
        .table("tasks")
        .insert(payload.model_dump(mode="json"))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to create task",
        )

    return response.data[0]


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    user_id: UUID = Query(...),
    scheduled_date: str | None = None,
    status: str | None = None,
):
    query = (
        supabase
        .table("tasks")
        .select("*")
        .eq("user_id", str(user_id))
    )

    if scheduled_date:
        query = query.eq(
            "scheduled_date",
            scheduled_date,
        )

    if status:
        query = query.eq(
            "status",
            status,
        )

    response = (
        query
        .order("plan_order", nullsfirst=False)
        .order("priority", desc=True)
        .execute()
    )

    return response.data


@router.get("/today", response_model=list[TaskResponse])
def get_today_tasks(user_id: UUID):
    today = date.today().isoformat()
    response = (
            supabase
            .table("tasks")
            .select("*")
            .eq("user_id", str(user_id))
            .eq("scheduled_date", today)
            .not_.in_("status", ["done", "cancelled"])
            .order("plan_order", nullsfirst=False)
            .order("priority", desc=True)
            .execute()
        )

    return response.data


@router.get("/today/progress", response_model=TodayProgressResponse)
def get_today_progress(
    user_id: UUID = Query(...),
):
    today = date.today().isoformat()

    response = (
        supabase
        .table("tasks")
        .select("id, status")
        .eq("user_id", str(user_id))
        .eq("scheduled_date", today)
        .not_.in_("status", ["cancelled", "skipped"])
        .execute()
    )

    tasks = response.data or []

    total = len(tasks)

    completed = sum(
        1
        for task in tasks
        if task["status"] == "done"
    )

    remaining = total - completed

    completion_rate = (
        round((completed / total) * 100, 2)
        if total > 0
        else 0.0
    )

    return {
        "date": today,
        "total": total,
        "completed": completed,
        "remaining": remaining,
        "completion_rate": completion_rate,
    }


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID):
    response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("id", str(task_id))
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return response.data


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
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

    if updates.get("status") == "done":
        updates["completed_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

    elif updates.get("status") in {
        "pending",
        "in_progress",
        "rescheduled",
    }:
        updates["completed_at"] = None

    response = (
        supabase
        .table("tasks")
        .update(updates)
        .eq("id", str(task_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return response.data[0]

@router.delete("/{task_id}")
def delete_task(task_id: UUID):
    response = (
        supabase
        .table("tasks")
        .delete()
        .eq("id", str(task_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "message": "Task deleted",
        "id": str(task_id),
    }
