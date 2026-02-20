"""
indexes.py
──────────
Crea los índices necesarios en la colección para optimizar
las agregaciones del dashboard.

  coffee_name → Gráfica 1 (agrupación por tipo de café)
  money       → KPI 1 (sum total de ingresos) y KPI 3 (avg/min/max)
  cash_type   → Gráfica 3 (agrupación por método de pago)
"""

from pymongo.collection import Collection


def create_indexes(collection: Collection) -> None:
    """Crea índices en los campos usados por las agregaciones."""
    # Gráfica 1: agrupación por tipo de café
    collection.create_index("coffee_name", name="idx_coffee_name")
    # Índice compuesto para Gráfica 1 con ingresos por café
    collection.create_index(
        [("coffee_name", 1), ("money", 1)],
        name="idx_coffee_name_money",
    )
    # Gráfica 3 y KPI 3: agrupación por método de pago
    collection.create_index("cash_type", name="idx_cash_type")
    collection.create_index("money", name="idx_money")
    # Índice compuesto para la agregación de Gráfica 3 con ingresos
    collection.create_index(
        [("cash_type", 1), ("money", 1)],
        name="idx_cash_type_money",
    )
    print(
        "  Índices creados: idx_coffee_name, idx_coffee_name_money, "
        "idx_cash_type, idx_money, idx_cash_type_money"
    )
