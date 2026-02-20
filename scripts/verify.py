"""
scripts/verify.py
─────────────────
Valida las agregaciones contra MongoDB.

Incluye:
  - KPI 2  → Total de Transacciones
  - KPI 3  → Ticket Promedio por Venta
  - Gráfica 2 → Ingresos por Mes
  - Gráfica 3 → Método de Pago

Uso
───
  source .venv/bin/activate
  python scripts/verify.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.aggregations.queries import (
    average_ticket,
    sales_by_payment,
    total_transactions,
    revenue_by_month,
)
from src.config.settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI
from src.ingestion.bulk_writer import get_collection


def main() -> None:
    collection = get_collection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

    # ────────────────────────────────────────────────────────────
    # KPI 2: Total de Transacciones
    # ────────────────────────────────────────────────────────────
    print("─── KPI 2: Total de Transacciones ─────────────────────────")
    total = total_transactions(collection)
    print(f"  Total: {total}")

    # ────────────────────────────────────────────────────────────
    # KPI 3: Ticket Promedio
    # ────────────────────────────────────────────────────────────
    ticket = average_ticket(collection)

    print("\n─── KPI 3: Ticket Promedio por Venta ─────────────────────")
    print(f"  Global:  {ticket['global']:>8.2f}")
    print()

    for row in ticket["by_payment"]:
        print(
            f"  {row['cash_type']:<8}"
            f"  avg={row['avg']:>7.2f}"
            f"  min={row['min']:>7.2f}"
            f"  max={row['max']:>7.2f}"
            f"  n={row['count']:>5}"
        )

    # ────────────────────────────────────────────────────────────
    # Gráfica 2: Ingresos por Mes
    # ────────────────────────────────────────────────────────────
    print("\n─── Gráfica 2: Ingresos por Mes ───────────────────────────")
    for row in revenue_by_month(collection):
        print(
            f"  {row['year']}-{row['month']:02d}"
            f"  ingresos={row['ingresos']:>10.2f}"
        )

    # ────────────────────────────────────────────────────────────
    # Gráfica 3: Método de Pago
    # ────────────────────────────────────────────────────────────
    print("\n─── Gráfica 3: Método de Pago (Donut) ────────────────────")
    for row in sales_by_payment(collection):
        print(
            f"  {row['cash_type']:<8}"
            f"  count={row['count']:>5}  ({row['pct_count']:>5.1f}%)"
            f"  ingresos={row['ingresos']:>9.2f}  ({row['pct_ingresos']:>5.1f}%)"
        )


if __name__ == "__main__":
    main()