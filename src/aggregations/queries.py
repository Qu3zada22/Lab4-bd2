"""
queries.py
──────────
Pipelines de agregación para las gráficas y KPIs del dashboard.

  Gráfica 1 — Ventas por tipo de café (Bar Chart)
  Gráfica 3 — Método de pago: Efectivo vs Tarjeta (Donut/Pie Chart)
  KPI 1     — Ingresos Totales
  KPI 3     — Ticket Promedio por Venta
"""

from pymongo.collection import Collection


def sales_by_coffee(collection: Collection) -> list[dict]:
    """
    Gráfica 1 — Ventas agrupadas por tipo de café (Bar Chart).

    Retorna por cada coffee_name:
      - count    : número de ventas
      - ingresos : suma total de money
    Ordenado de mayor a menor cantidad de ventas.
    """
    pipeline = [
        # Agrupar por nombre del café
        {
            "$group": {
                "_id": "$coffee_name",
                "count": {"$sum": 1},
                "ingresos": {"$sum": "$money"},
            }
        },
        # Proyectar campos legibles
        {
            "$project": {
                "_id": 0,
                "coffee_name": "$_id",
                "count": "$count",
                "ingresos": {"$round": ["$ingresos", 2]},
            }
        },
        # De mayor a menor ventas (eje Y del Bar Chart)
        {"$sort": {"count": -1}},
    ]
    return list(collection.aggregate(pipeline))


def total_revenue(collection: Collection) -> float:
    """
    KPI 1 — Ingresos Totales: suma de todos los valores de money.

    Retorna un float con el total redondeado a 2 decimales.
    """
    result = list(
        collection.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$money"}}},
            {"$project": {"_id": 0, "total": {"$round": ["$total", 2]}}},
        ])
    )
    return result[0]["total"] if result else 0.0


def sales_by_payment(collection: Collection) -> list[dict]:
    """
    Gráfica 3 — Distribución de transacciones por método de pago.

    Retorna por cada cash_type:
      - count       : número de transacciones
      - ingresos    : suma total de money
      - pct_count   : porcentaje de transacciones sobre el total
      - pct_ingresos: porcentaje de ingresos sobre el total
    """
    pipeline = [
        # Paso 1: agrupar por método de pago
        {
            "$group": {
                "_id": "$cash_type",
                "count": {"$sum": 1},
                "ingresos": {"$sum": "$money"},
            }
        },
        # Paso 2: acumular totales para calcular porcentajes
        {
            "$group": {
                "_id": None,
                "methods": {"$push": "$$ROOT"},
                "total_count": {"$sum": "$count"},
                "total_ingresos": {"$sum": "$ingresos"},
            }
        },
        # Paso 3: desanidar cada método
        {"$unwind": "$methods"},
        # Paso 4: proyectar campos finales con porcentajes redondeados
        {
            "$project": {
                "_id": 0,
                "cash_type": "$methods._id",
                "count": "$methods.count",
                "ingresos": {"$round": ["$methods.ingresos", 2]},
                "pct_count": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$methods.count", "$total_count"]}, 100]},
                        1,
                    ]
                },
                "pct_ingresos": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$methods.ingresos", "$total_ingresos"]}, 100]},
                        1,
                    ]
                },
            }
        },
        {"$sort": {"count": -1}},
    ]
    return list(collection.aggregate(pipeline))


def average_ticket(collection: Collection) -> dict:
    """
    KPI 3 — Ticket promedio global y desglosado por método de pago.

    Retorna:
      {
        "global": float,                        ← promedio global
        "by_payment": [                         ← desglose por método
          { "cash_type", "avg", "min", "max", "count" },
          ...
        ]
      }
    """
    # Promedio global
    global_result = list(
        collection.aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$money"}}},
            {"$project": {"_id": 0, "avg": {"$round": ["$avg", 2]}}},
        ])
    )
    global_avg = global_result[0]["avg"] if global_result else 0.0

    # Desglose por método de pago
    by_payment = list(
        collection.aggregate([
            {
                "$group": {
                    "_id": "$cash_type",
                    "avg": {"$avg": "$money"},
                    "min": {"$min": "$money"},
                    "max": {"$max": "$money"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "cash_type": "$_id",
                    "avg": {"$round": ["$avg", 2]},
                    "min": "$min",
                    "max": "$max",
                    "count": "$count",
                }
            },
            {"$sort": {"cash_type": 1}},
        ])
    )

    return {"global": global_avg, "by_payment": by_payment}
