from typing import List, Optional

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from ..utils import get_collection
from .models import StockItemDAO, StockItemMetaDAO
from .schemas import StockItemMeta


def get_estoque_atual_cd(codCd: int) -> List[StockItemMetaDAO]:
    collection = get_collection(StockItemMetaDAO.collection_name())
    items = collection.find({"codCd": codCd})
    return [StockItemMetaDAO(**item) for item in items]


def entrada_estoque_cd(codCd: int, item: StockItemMeta) -> StockItemMetaDAO:
    item_dao = StockItemMetaDAO(**item.model_dump(), codCd=codCd)
    collection = get_collection(StockItemMetaDAO.collection_name())
    try:
        collection.insert_one(item_dao.model_dump(by_alias=True))
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Item already exists in stock")

    return item_dao


def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    collection = get_collection(StockItemMetaDAO.collection_name())
    result = collection.update_one(
        {"codCd": codCd, "codBarras": codBarras, "qtdAtual": {"$gte": qtd}},
        {"$inc": {"qtdAtual": -qtd}},
    )
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail="Item not found or insufficient quantity"
        )


def get_estoque_historico_cd(
    codCd: int, since: Optional[str] = None
) -> List[StockItemMetaDAO]:
    collection = get_collection(StockItemMetaDAO.collection_name())
    query = {"codCd": codCd}
    if since:
        query = {"codCD": codCd, "$gte": since}  # TODO ramiro review this please
    items = collection.find(query)
    return [StockItemMetaDAO(**item) for item in items]
