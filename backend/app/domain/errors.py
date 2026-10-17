"""Excepciones del dominio. Heredan de ValueError para errores de datos o de regla."""

__all__ = ["DomainError"]


class DomainError(ValueError):
    """Dato o regla de negocio inválidos; el mensaje sale del catálogo."""
