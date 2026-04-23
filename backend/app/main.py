from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__


def create_app() -> FastAPI:
    app = FastAPI(
        title="TechReport from YouTube — API",
        version=__version__,
        description="YouTube keyword search + transcript analysis → Korean tech report (Markdown).",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": "techreport-backend", "version": __version__}

    return app


app = create_app()
