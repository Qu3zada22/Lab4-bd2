"""
scripts/verify.py
─────────────────
Corre las agregaciones contra MongoDB e imprime un resumen en consola.
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
    revenue_by_month,
    sales_by_coffee,
    sales_by_payment,
    total_revenue,
    total_transactions,
)
from src.config.settings import MONGO_COLLECTION, MONGO_DB, MONGO_URI
from src.ingestion.bulk_writer import get_collection


def main() -> None:
    collection = get_collection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

    print("─── KPIs ────────────────────────────────────────────")
    print(f"  KPI 1 – Ingresos Totales:    {total_revenue(collection):>12,.2f}")
    print(f"  KPI 2 – Total Transacciones: {total_transactions(collection):>12,}")
    print(f"  KPI 3 – Ticket Promedio:     {average_ticket(collection):>12,.2f}")

    print("\n─── Gráfica 1: Ventas por tipo de café ──────────────")
    for row in sales_by_coffee(collection):
        print(f"  {row['_id']:<30}  ventas={row['total_ventas']:>5}  ingresos={row['ingresos']:>8.2f}")

    print("\n─── Gráfica 2: Ingresos por mes ─────────────────────")
    for row in revenue_by_month(collection):
        print(f"  {row['_id']}  ingresos={row['ingresos']:>10.2f}  tx={row['transacciones']:>5}")

    print("\n─── Gráfica 3: Método de pago ───────────────────────")
    for row in sales_by_payment(collection):
        print(f"  {row['_id']:<10}  count={row['count']:>5}  ingresos={row['ingresos']:>8.2f}")


if __name__ == "__main__":
    main()
