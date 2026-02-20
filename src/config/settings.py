"""
settings.py
───────────
Carga variables de entorno desde .env y las expone como constantes tipadas.

Para cambiar de Docker local a Atlas:
  1. Detener docker-compose (`docker compose down`)
  2. Cambiar MONGO_URI en .env por la connection string de Atlas
  3. Volver a correr el script de ingesta — sin tocar código.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")

# MongoDB
MONGO_URI: str = os.environ["MONGO_URI"]
MONGO_DB: str = os.getenv("MONGO_DB", "coffee_sales")
MONGO_COLLECTION: str = os.getenv("MONGO_COLLECTION", "sales")

# Datos crudos
DATA_DIR: Path = Path(os.getenv("DATA_DIR", str(_root / "data")))
