from datetime import datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query

from app.supabase import supabase


router = APIRouter(
    prefix="/planning-context",
    tags=["Planning Context"],
)


@router.get("")
def get_planning_context(
    user_id: UUID = Query(...),
):
    # =====================================================
    # 1. Get user's timezone
    # =====================================================

    user_response = (
        supabase
        .table("users")
        .select("timezone")
        .eq("id", str(user_id))
        .single()
        .execute()
    )

    user = user_response.data

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    timezone_name = user.get(
        "timezone",
        "Asia/Jakarta",
    )

    try:
        user_timezone = ZoneInfo(timezone_name)
    except Exception:
        user_timezone = ZoneInfo("Asia/Jakarta")

    now = datetime.now(user_timezone)

    today = now.date()
    recent_start = today - timedelta(days=6)

    # =====================================================
    # 2. Active missions
    # =====================================================

    missions_response = (
        supabase
        .table("missions")
        .select("*")
        .eq("user_id", str(user_id))
        .eq("status", "active")
        .order("priority", desc=True)
        .order("deadline")
        .execute()
    )

    missions = missions_response.data or []

    # =====================================================
    # 3. Active milestones
    # =====================================================

    mission_ids = [
        mission["id"]
        for mission in missions
    ]

    milestones = []

    if mission_ids:
        milestones_response = (
            supabase
            .table("milestones")
            .select("*")
            .in_("mission_id", mission_ids)
            .in_(
                "status",
                ["pending", "active", "blocked"],
            )
            .order("order_index")
            .execute()
        )

        milestones = milestones_response.data or []

    # =====================================================
    # 4. Active projects
    # =====================================================

    projects = []

    if mission_ids:
        projects_response = (
            supabase
            .table("projects")
            .select("*")
            .in_("mission_id", mission_ids)
            .in_(
                "status",
                ["planned", "active", "blocked"],
            )
            .order("priority", desc=True)
            .execute()
        )

        projects = projects_response.data or []

    # =====================================================
    # 5. Today's tasks
    # =====================================================

    tasks_response = (
        supabase
        .table("tasks")
        .select("*")
        .eq("user_id", str(user_id))
        .eq(
            "scheduled_date",
            today.isoformat(),
        )
        .not_.in_(
            "status",
            ["cancelled"],
        )
        .order(
            "plan_order",
            nullsfirst=False,
        )
        .order(
            "priority",
            desc=True,
        )
        .execute()
    )

    today_tasks = tasks_response.data or []

    # =====================================================
    # 6. Recent daily context
    # =====================================================

    daily_logs_response = (
        supabase
        .table("daily_logs")
        .select("*")
        .eq("user_id", str(user_id))
        .gte(
            "log_date",
            recent_start.isoformat(),
        )
        .lte(
            "log_date",
            today.isoformat(),
        )
        .order(
            "log_date",
            desc=True,
        )
        .execute()
    )

    recent_daily_context = (
        daily_logs_response.data or []
    )

    # =====================================================
    # 7. Recent habit signals
    # =====================================================

    habits_response = (
        supabase
        .table("habit_signals")
        .select("*")
        .eq("user_id", str(user_id))
        .gte(
            "signal_date",
            recent_start.isoformat(),
        )
        .lte(
            "signal_date",
            today.isoformat(),
        )
        .order(
            "signal_date",
            desc=True,
        )
        .execute()
    )

    habit_signals = (
        habits_response.data or []
    )

    # =====================================================
    # 8. Return planning context
    # =====================================================

    return {
        "generated_at": now.isoformat(),
        "timezone": timezone_name,
        "today": today.isoformat(),

        "missions": missions,

        "milestones": milestones,

        "projects": projects,

        "today_tasks": today_tasks,

        "recent_daily_context": recent_daily_context,

        "habit_signals": habit_signals,
    }