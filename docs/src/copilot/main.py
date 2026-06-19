"""FastAPI application entrypoint (the 'walking skeleton')."""

from fastapi import FastAPI

app = FastAPI(title="AI Landscaping Copilot", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Returns 200 if the service is up."""
    return {"status": "ok"}
