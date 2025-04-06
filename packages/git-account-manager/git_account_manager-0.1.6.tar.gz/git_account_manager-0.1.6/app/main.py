from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.database import create_db_and_tables

from . import __version__

prefix = "/api"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Git Account Manager API",
    description="""
    A tool to manage multiple Git accounts and projects.

    Features:
    - Manage multiple Git accounts (personal/work)
    - Configure SSH keys for different accounts
    - Associate Git projects with specific accounts
    - Synchronize SSH configurations
    """,
    version=__version__,
    contact={
        "name": "NourEldin",
        "email": "noureldin.osama.saad@gmail.com",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],  # Next.js default, FastAPI default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=prefix)

# Set the static directory to serve frontend files
STATIC_DIRS = [
    Path(__file__).resolve().parent.parent.parent / "frontend" / "dist",
    # add static directory within app directory
    Path(__file__).resolve().parent / "static",
]

STATIC_DIR = None
for static_dir in STATIC_DIRS:
    if static_dir.exists():
        STATIC_DIR = static_dir
        break
else:
    raise FileNotFoundError("Static directory not found.")


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


def main() -> None:
    """Start the FastAPI application server.

    This function initializes and starts the FastAPI server with the following configuration:
    - Host: 127.0.0.1 (localhost)
    - Port: 8000
    """
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
