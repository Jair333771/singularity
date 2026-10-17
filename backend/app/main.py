"""Fábrica de la aplicación FastAPI que expone el motor de preguntas por HTTP."""

from fastapi import FastAPI

__all__ = ["create_app"]


def create_app() -> FastAPI:
    """Crea la aplicación con sus rutas y dependencias."""
    return FastAPI(title="api.singularity", description="Motor de preguntas de Singularity", version="0.1.0")
