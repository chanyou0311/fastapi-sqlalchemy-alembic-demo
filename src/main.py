from fastapi import FastAPI

from .routers import projects

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(projects.router)
