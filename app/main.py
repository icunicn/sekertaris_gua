from fastapi import FastAPI, Depends
from app.security import require_api_key


from app.routers import missions
from app.routers import milestones
from app.routers import projects
from app.routers import tasks
from app.routers import context
from app.routers import daily_context
from app.routers import habits
from app.routers import planning_context


app = FastAPI(
    title="Orbit API",
    version="0.1.0",
    description="Execution layer for Orbit Personal OS",
)


@app.get("/")
def root():
    return {
        "name": "Orbit API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "orbit-api",
    }


app.include_router(missions.router, dependencies=[Depends(require_api_key)])
app.include_router(milestones.router, dependencies=[Depends(require_api_key)])
app.include_router(projects.router, dependencies=[Depends(require_api_key)])
app.include_router(tasks.router, dependencies=[Depends(require_api_key)])
app.include_router(context.router, dependencies=[Depends(require_api_key)])
app.include_router(daily_context.router, dependencies=[Depends(require_api_key)])
app.include_router(habits.router, dependencies=[Depends(require_api_key)])
app.include_router(planning_context.router, dependencies=[Depends(require_api_key)])
