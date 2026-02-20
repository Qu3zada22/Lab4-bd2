"""
sale.py
───────
Dataclass que representa un documento de venta en MongoDB.

Maneja las diferencias de esquema entre index_1.csv e index_2.csv:
  - index_1 tiene columna `card` (ID de tarjeta anonimizado)
  - index_2 no la tiene
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Sale:
    date: datetime        # fecha de la transacción
    datetime_: datetime   # timestamp completo
    cash_type: str        # "card" | "cash"
    money: float          # monto de la transacción
    coffee_name: str      # nombre del producto
    card: Optional[str] = None  # ID anonimizado (solo index_1)

    @property
    def year_month(self) -> str:
        """Devuelve 'YYYY-MM' para agrupar por mes en agregaciones."""
        return self.date.strftime("%Y-%m")

    def to_document(self) -> dict:
        """Convierte el dataclass a un dict listo para MongoDB."""
        doc = {
            "date": self.date,
            "datetime": self.datetime_,
            "cash_type": self.cash_type,
            "money": self.money,
            "coffee_name": self.coffee_name,
            "year_month": self.year_month,
        }
        if self.card is not None:
            doc["card"] = self.card
        return doc
