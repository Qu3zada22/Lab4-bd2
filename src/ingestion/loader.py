"""
loader.py
─────────
Lee todos los archivos CSV de DATA_DIR y devuelve una lista de objetos Sale.
Maneja las diferencias de esquema entre index_1.csv e index_2.csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.models.sale import Sale


def load_csv(path: Path) -> list[Sale]:
    """Parsea un CSV individual y retorna una lista de Sale."""
    df = pd.read_csv(path, parse_dates=["date", "datetime"])
    has_card = "card" in df.columns

    sales: list[Sale] = []
    for _, row in df.iterrows():
        sales.append(
            Sale(
                date=row["date"].to_pydatetime(),
                datetime_=row["datetime"].to_pydatetime(),
                cash_type=row["cash_type"].strip().lower(),
                money=float(row["money"]),
                coffee_name=row["coffee_name"].strip(),
                card=str(row["card"]) if has_card and pd.notna(row["card"]) else None,
            )
        )
    return sales


def load_all(data_dir: Path) -> list[Sale]:
    """Carga todos los *.csv encontrados en data_dir."""
    files = sorted(data_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos CSV en {data_dir}")

    all_sales: list[Sale] = []
    for f in files:
        print(f"  Cargando {f.name} …")
        batch = load_csv(f)
        print(f"    → {len(batch)} registros")
        all_sales.extend(batch)

    print(f"\n  Total cargado: {len(all_sales)} registros")
    return all_sales
