from uuid import UUID

from fastapi import APIRouter, Query

from app.supabase import supabase


router = APIRouter(
    prefix="/habits",
    tags=["Habits"],
)


@router.get("")
def get_habits(
    user_id: UUID = Query(...),
    habit_key: str | None = None,
    limit: int = Query(default=30, ge=1, le=100),
):
    query = (
        supabase
        .table("habit_signals")
        .select("*")
        .eq("user_id", str(user_id))
    )

    if habit_key:
        query = query.eq(
            "habit_key",
            habit_key,
        )

    response = (
        query
        .order("signal_date", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data
