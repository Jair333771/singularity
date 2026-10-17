"""Catálogo de mensajes que resuelve Info a texto."""

from app.domain.messages import Info

__all__ = ["InfoCatalog"]


class InfoCatalog:
    """Implementa MessageCatalog sobre un diccionario de textos por clave."""

    def __init__(self, messages: dict[str, str]) -> None:
        self._messages = {Info[key]: text for key, text in messages.items()}
        missing = [info.name for info in Info if info not in self._messages]
        if missing:
            raise ValueError(f"info file missing keys: {', '.join(missing)}")

    def text(self, info: Info, **params: object) -> str:
        """Devuelve el mensaje con sus parámetros nombrados sustituidos."""
        return self._messages[info].format(**params)
