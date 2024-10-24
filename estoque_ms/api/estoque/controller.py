from typing import List

from fastapi import HTTPException
from pymongo.errors import BulkWriteError, DuplicateKeyError

from ..utils import get_collection
from .models import StockItemDAO


def get_estoque_atual_cd(codCd: int) -> List[StockItemDAO]:
    collection = get_collection(StockItemDAO.collection_name())
    items = collection.find({"codCd": codCd})
    return [StockItemDAO(**item) for item in items]


def entrada_estoque_cd(codCd: int, items: List[StockItemDAO]) -> List[StockItemDAO]:
    if not items:
        raise HTTPException(status_code=400, detail="No items to add")

    collection = get_collection(StockItemDAO.collection_name())

    items_dict = [item.model_dump(by_alias=True) for item in items]

    try:
        collection.insert_many(items_dict)
    except (DuplicateKeyError, BulkWriteError) as e:
        if isinstance(e, DuplicateKeyError):
            raise HTTPException(
                status_code=409,
                detail=f"One or more items already exist in stock details: {e.details}",
            )

        if isinstance(e, BulkWriteError):
            raise HTTPException(
                status_code=400,
                detail=f"One or more items already exist in stock details: {e.details}",
            )

    return items


def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    collection = get_collection(StockItemDAO.collection_name())
    result = collection.update_one(
        {"codCd": codCd, "codBarras": codBarras, "qtdAtual": {"$gte": qtd}},
        {"$inc": {"qtdAtual": -qtd}},
    )
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail="Item not found or insufficient quantity"
        )


def get_item_cd(codCd: int, nome: str) -> List[StockItemDAO]:
    collection = get_collection(StockItemDAO.collection_name())
    items = collection.find({"codCd": codCd, "nome": nome})

    return [StockItemDAO(**item) for item in items]
