from typing import List

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

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

    # TODO: fix concurrency issue
    for item in items_dict:
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            collection.update_one(
                {"codCd": codCd, "nome": item["nome"]},
                {"$inc": {"quantidade": item["quantidade"]}},
            )

    updated_items = collection.find(
        {"codCd": codCd, "nome": {"$in": [item["nome"] for item in items_dict]}}
    )
    return [StockItemDAO(**item) for item in updated_items]


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
