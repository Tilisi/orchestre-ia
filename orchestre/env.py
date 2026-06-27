"""
Chargement robuste de la configuration d'environnement.

Objectif : le CLI doit fonctionner même si python-dotenv n'est pas encore
installé. Si python-dotenv est disponible, on l'utilise. Sinon, on charge
un fichier .env simple sans dépendance externe.
"""

from __future__ import annotations

import os
from pathlib import Path


def _parse_env_line(line: str) -> tuple[str, str] | None:
    """Parse une ligne KEY=VALUE simple d'un fichier .env."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None
    key, _, value = stripped.partition("=")
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


def load_env(path: str | os.PathLike[str] | None = None, *, override: bool = False) -> None:
    """
    Charge un fichier .env.

    - N'échoue pas si le fichier n'existe pas.
    - Utilise python-dotenv si installé.
    - Fallback manuel si python-dotenv est absent.
    - Par défaut, ne remplace pas les variables déjà présentes.
    """
    env_path = Path(path or ".env")
    if not env_path.exists():
        return

    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(env_path, override=override)
        return
    except ImportError:
        pass

    with env_path.open(encoding="utf-8") as handle:
        for line in handle:
            parsed = _parse_env_line(line)
            if not parsed:
                continue
            key, value = parsed
            if override or key not in os.environ:
                os.environ[key] = value
