"""
queries.py
──────────
Pipelines de agregación para los charts y KPIs del dashboard.

Dashboard (docs/todos.md):
  Gráfica 1 — Ventas por tipo de café        (Bar Chart)
  Gráfica 2 — Ingresos por mes               (Line Chart)
  Gráfica 3 — Método de pago: Efectivo/Tarjeta (Donut/Pie)
  KPI 1     — Ingresos Totales
  KPI 2     — Total de Transacciones
  KPI 3     — Ticket Promedio por Venta
"""

from pymongo.collection import Collection


# ─── Gráficas ─────────────────────────────────────────────────────────────────

def sales_by_coffee(collection: Collection) -> list[dict]:
    """Gráfica 1 — ventas y revenue agrupados por tipo de café."""
    pipeline = [
        {
            "$group": {
                "_id": "$coffee_name",
                "total_ventas": {"$sum": 1},
                "ingresos": {"$sum": "$money"},
            }
        },
        {"$sort": {"total_ventas": -1}},
    ]
    return list(collection.aggregate(pipeline))


def revenue_by_month(collection: Collection) -> list[dict]:
    """Gráfica 2 — ingresos totales por mes (YYYY-MM)."""
    pipeline = [
        {
            "$group": {
                "_id": "$year_month",
                "ingresos": {"$sum": "$money"},
                "transacciones": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]
    return list(collection.aggregate(pipeline))


def sales_by_payment(collection: Collection) -> list[dict]:
    """Gráfica 3 — conteo de transacciones por método de pago."""
    pipeline = [
        {
            "$group": {
                "_id": "$cash_type",
                "count": {"$sum": 1},
                "ingresos": {"$sum": "$money"},
            }
        },
        {"$sort": {"count": -1}},
    ]
    return list(collection.aggregate(pipeline))


# ─── KPIs ─────────────────────────────────────────────────────────────────────

def total_revenue(collection: Collection) -> float:
    """KPI 1 — suma total de todos los montos."""
    result = list(
        collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$money"}}}])
    )
    return result[0]["total"] if result else 0.0


def total_transactions(collection: Collection) -> int:
    """KPI 2 — número total de documentos en la colección."""
    return collection.count_documents({})


def average_ticket(collection: Collection) -> float:
    """KPI 3 — valor promedio por transacción."""
    result = list(
        collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$money"}}}])
    )
    return round(result[0]["avg"], 2) if result else 0.0
