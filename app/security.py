from typing import Annotated

from fastapi import Header, HTTPException

from app.config import settings


async def require_api_key(
    x_orbit_key: Annotated[
        str | None,
        Header()
    ] = None,
):
    if (
        not settings.orbit_api_key
        or x_orbit_key != settings.orbit_api_key
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Orbit API key",
        )