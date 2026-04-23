"""TechReport from YouTube — backend package.

The package layout follows the TechSpec §6-2 layered design:

    app/
    ├── api/            # HTTP routes
    ├── services/       # Use-case orchestration
    ├── pipeline/       # Retrieval → Analysis → Rendering pipeline steps
    ├── ports/          # Abstract ports (LLM, YouTube search, transcript)
    ├── adapters/       # Concrete adapters (Claude, YouTube Data, transcript)
    ├── repository/     # File I/O for generated reports
    ├── schemas.py      # Pydantic DTOs shared across layers
    ├── config.py       # Settings (env-var backed)
    └── main.py         # FastAPI application factory
"""

__version__ = "0.1.0"
