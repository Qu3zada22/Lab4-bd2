"""
queries.py
──────────
Pipelines de agregación para Gráfica 3 y KPI 3.

  Gráfica 3 — Método de pago: Efectivo vs Tarjeta (Donut/Pie Chart)
  KPI 3     — Ticket Promedio por Venta
"""

from pymongo.collection import Collection






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


def total_transactions(collection: Collection) -> int:
    """
    KPI 2 — Total de transacciones.
    Retorna el número total de documentos en la colección.
    """
    return collection.count_documents({}) 


def revenue_by_month(collection: Collection) -> list[dict]:
    """
    Gráfica 2 — Ingresos por mes (Line Chart)

    Retorna:
      [
        {
          "year": 2023,
          "month": 1,
          "ingresos": 12345.67
        },
        ...
      ]
    """
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                },
                "ingresos": {"$sum": "$money"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "ingresos": {"$round": ["$ingresos", 2]},
            }
        },
        {
            "$sort": {
                "year": 1,
                "month": 1,
            }
        },
    ]

    return list(collection.aggregate(pipeline))