"""
bulk_writer.py
──────────────
Escribe documentos Sale en MongoDB usando bulk_write (InsertOne por lotes).
ordered=False permite que un documento malo no detenga el lote completo.
"""

from __future__ import annotations

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.operations import InsertOne

from src.models.sale import Sale


def get_collection(uri: str, db_name: str, collection_name: str) -> Collection:
    """Crea un MongoClient y retorna la colección objetivo."""
    client: MongoClient = MongoClient(uri)
    return client[db_name][collection_name]


def bulk_insert(
    collection: Collection,
    sales: list[Sale],
    batch_size: int = 500,
) -> int:
    """
    Inserta ventas en lotes usando bulk_write.
    Retorna el total de documentos insertados.
    """
    total = 0
    batch: list[InsertOne] = []

    for sale in sales:
        batch.append(InsertOne(sale.to_document()))

        if len(batch) >= batch_size:
            result = collection.bulk_write(batch, ordered=False)
            total += result.inserted_count
            batch = []

    if batch:
        result = collection.bulk_write(batch, ordered=False)
        total += result.inserted_count

    return total
