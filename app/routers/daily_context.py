from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.supabase import supabase


router = APIRouter(
    prefix="/daily-context",
    tags=["Daily Context"],
)


@router.get("")
def get_daily_context(
    user_id: UUID = Query(...),
    log_date: date | None = None,
):
    query = (
        supabase
        .table("daily_logs")
        .select("*")
        .eq("user_id", str(user_id))
    )

    if log_date is not None:
        query = query.eq(
            "log_date",
            log_date.isoformat(),
        )

    response = (
        query
        .order("log_date", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Daily context not found",
        )

    return response.data[0]