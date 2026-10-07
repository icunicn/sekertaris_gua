from fastapi import APIRouter, HTTPException
from uuid import UUID


from app.models.context import ContextPacket
from app.supabase import supabase


router = APIRouter(
    prefix="/context",
    tags=["Context"],
)


@router.post("")
def create_context_packet(
    payload: ContextPacket,
):
    data = {
        "user_id": str(payload.user_id),
        "packet_type": payload.type,
        "effective_date": (
            payload.effective_date.isoformat()
            if payload.effective_date
            else None
        ),
        "payload": payload.model_dump(
            mode="json"
        ),
    }

    response = (
        supabase
        .table("context_packets")
        .insert(data)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to store context packet",
        )

    return response.data[0]


@router.post("/{context_id}/apply")
def apply_context_packet(
    context_id: UUID,
):
    packet_response = (
        supabase
        .table("context_packets")
        .select("packet_type, applied_at")
        .eq("id", str(context_id))
        .single()
        .execute()
    )

    packet = packet_response.data

    if not packet:
        raise HTTPException(
            status_code=404,
            detail="Context packet not found",
        )

    if packet["applied_at"] is not None:
        raise HTTPException(
            status_code=409,
            detail="Context packet has already been applied",
        )

    packet_type = packet["packet_type"]

    if packet_type == "daily_context":
        rpc_name = "apply_daily_context_packet"

    elif packet_type == "mission_create":
        rpc_name = "apply_context_packet"

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported context packet type: {packet_type}",
        )

    response = (
        supabase
        .rpc(
            rpc_name,
            {
                "p_context_id": str(context_id),
            },
        )
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to apply context packet",
        )

    return response.data
