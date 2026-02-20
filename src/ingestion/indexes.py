"""
indexes.py
──────────
Crea los índices necesarios en la colección para optimizar
las agregaciones de Gráfica 3 y KPI 3.

  cash_type → Gráfica 3 (agrupación por método de pago)
  money     → KPI 3 (avg/min/max de montos)
"""

from pymongo.collection import Collection


def create_indexes(collection: Collection) -> None:
    """Crea índices en los campos usados por las agregaciones."""
    collection.create_index("cash_type", name="idx_cash_type")
    collection.create_index("money", name="idx_money")
    # Índice compuesto para la agregación de Gráfica 3 con ingresos
    collection.create_index(
        [("cash_type", 1), ("money", 1)],
        name="idx_cash_type_money",
    )
    print("  Índices creados: idx_cash_type, idx_money, idx_cash_type_money")
