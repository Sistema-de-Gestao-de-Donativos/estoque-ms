from typing import List

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from ..utils import get_collection
from .models import StockItemDAO
from .schemas import StockItem


def get_estoque_atual_cd(codCd: int) -> List[StockItemDAO]:
    collection = get_collection(StockItemDAO.collection_name())
    items = collection.find({"codCd": codCd})
    return [StockItemDAO(**item) for item in items]


def entrada_estoque_cd(codCd: int, items: List[StockItem]):
    for item in items:
        item_dao = StockItemDAO(**item.model_dump(), codCd=codCd)
        collection = get_collection(StockItemDAO.collection_name())
        try:
            collection.insert_one(item_dao.model_dump(by_alias=True))
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Item already exists in stock")

        return True


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
