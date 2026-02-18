from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.api.routes import router
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources
    print("Starting up Rescue Coordinator...")
    init_db()
    yield
    # Clean up resources
    print("Shutting down Rescue Coordinator...")

app = FastAPI(title="Rescue Coordinator API", lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Rescue Coordinator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
