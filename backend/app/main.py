"""Fábrica de la aplicación FastAPI que expone el motor de preguntas por HTTP."""

from fastapi import FastAPI

app = FastAPI(title="api.singularity", description="Motor de preguntas proyecto Singularity", version="0.1.0")

@app.get("/health", summary="Verifica el estado de la API preguntas", response_model=dict, tags=["Health"])
def health():
    return {"status": "200", "message": "OK"}
