"""
scripts/verify.py
─────────────────
Valida las agregaciones de todas las gráficas y KPIs contra MongoDB.
Usar después de ingest.py para confirmar que los datos están correctos.

Uso
───
  # uv
  uv run scripts/verify.py

  # venv
  source .venv/bin/activate
  python scripts/verify.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.aggregations.queries import (
    average_ticket,
    sales_by_coffee,
    sales_by_payment,
    total_revenue,
)
from src.config.settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI
from src.ingestion.bulk_writer import get_collection


def main() -> None:
    collection = get_collection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

    # KPI 1: Ingresos Totales
    revenue = total_revenue(collection)
    print("KPI 1: Ingresos Totales")
    print(f"Total:  {revenue:>10.2f}")

    # Gráfica 1: Ventas por tipo de café 
    print("\nGráfica 1: Ventas por tipo de café (Bar Chart)")
    for row in sales_by_coffee(collection):
        print(
            f"  {row['coffee_name']:<20}"
            f"  ventas={row['count']:>5}"
            f"  ingresos={row['ingresos']:>9.2f}"
        )

    #KPI 3: Ticket Promedio
    ticket = average_ticket(collection)
    print("\nKPI 3: Ticket Promedio por Venta")
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

    # Gráfica 3: Método de pago 
    print("\nGráfica 3: Método de pago (Donut)")
    for row in sales_by_payment(collection):
        print(
            f"  {row['cash_type']:<8}"
            f"  count={row['count']:>5}  ({row['pct_count']:>5.1f}%)"
            f"  ingresos={row['ingresos']:>9.2f}  ({row['pct_ingresos']:>5.1f}%)"
        )


if __name__ == "__main__":
    main()
