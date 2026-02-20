"""
scripts/ingest.py
─────────────────
Entry point: lee los CSVs de data/ y los escribe en MongoDB via bulk_write.

Uso
───
  # uv
  uv run scripts/ingest.py

  # venv
  source .venv/bin/activate
  python scripts/ingest.py

  # Limpieza previa (drop + reinsert)
  python scripts/ingest.py --drop
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config.settings import DATA_DIR, MONGO_COLLECTION, MONGO_DB, MONGO_URI
from src.ingestion.bulk_writer import bulk_insert, get_collection
from src.ingestion.indexes import create_indexes
from src.ingestion.loader import load_all


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta de datos CSV → MongoDB.")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Elimina la colección antes de insertar (clean run).",
    )
    args = parser.parse_args()

    print(f"URI:        {MONGO_URI}")
    print(f"Base:       {MONGO_DB}")
    print(f"Colección:  {MONGO_COLLECTION}")

    collection = get_collection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

    if args.drop:
        collection.drop()
        print("Colección eliminada.\n")

    print(f"Cargando CSVs desde: {DATA_DIR}\n")
    sales = load_all(DATA_DIR)

    print("\nEjecutando bulk_write …")
    inserted = bulk_insert(collection, sales)
    print(f"\nListo. {inserted} documentos insertados en {MONGO_DB}.{MONGO_COLLECTION}")

    print("\nCreando índices …")
    create_indexes(collection)


if __name__ == "__main__":
    main()
