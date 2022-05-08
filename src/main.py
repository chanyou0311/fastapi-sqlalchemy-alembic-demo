from fastapi import FastAPI

from .routers import projects, tasks

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(projects.router)
app.include_router(tasks.router)
