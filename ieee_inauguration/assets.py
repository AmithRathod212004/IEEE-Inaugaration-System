"""Helpers for event asset management."""

from pathlib import Path

from .config import ROOT_DIR


def resolve_asset(path: str) -> Path:
    """Resolve an asset path relative to project root."""

    return (ROOT_DIR / path).resolve()
