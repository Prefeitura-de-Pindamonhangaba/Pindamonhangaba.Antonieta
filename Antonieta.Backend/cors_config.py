import json
from typing import Optional


PRODUCTION_ORIGIN = "https://antonieta.pindamonhangaba.sp.gov.br"


def get_cors_origins(configured_origins: Optional[str]) -> list[str]:
    """Always allow the official frontend, plus explicitly configured origins."""
    configured = configured_origins if configured_origins is not None else "http://localhost:3000"
    if configured.strip().startswith("["):
        values = json.loads(configured)
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise ValueError("CORS_ORIGINS deve conter uma lista de strings")
    else:
        values = configured.split(",")
    origins = [origin.strip().rstrip("/") for origin in values if origin.strip()]
    if "*" in origins:
        raise ValueError("CORS_ORIGINS deve listar origens explícitas")
    return list(dict.fromkeys([PRODUCTION_ORIGIN, *origins]))
