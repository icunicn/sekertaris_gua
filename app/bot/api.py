import httpx

from app.config import settings

Headers = {
    "X-Orbit-Key": settings.orbit_api_key,
}

async def get_today_tasks():
    url = f"{settings.orbit_api_url}/tasks/today"

    params = {
        "user_id": settings.orbit_user_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers=Headers,
            timeout=10,
        )

    response.raise_for_status()

    return response.json()


async def get_today_progress():
    url = f"{settings.orbit_api_url}/tasks/today/progress"

    params = {
        "user_id": settings.orbit_user_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers=Headers,
            timeout=10,
        )

    response.raise_for_status()

    return response.json()


async def complete_task(task_id: str):
    url = f"{settings.orbit_api_url}/tasks/{task_id}"

    payload = {
        "status": "done",
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url,
            json=payload,
            headers=Headers,
            timeout=10,
        )

    response.raise_for_status()

    return response.json()
