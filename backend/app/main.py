from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.analyze import router as analyze_router
from app.api.health import router as health_router
from app.api.search import router as search_router


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

    app.include_router(health_router)
    app.include_router(search_router)
    app.include_router(analyze_router)

    return app


app = create_app()
