"""Validación de nombres para evitar inyección en argumentos de subprocess."""

import re

_IFACE_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+$")


def assert_safe_iface(name: str) -> None:
    if not name or not _IFACE_PATTERN.match(name):
        raise ValueError("Nombre de interfaz inválido.")
