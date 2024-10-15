import contextlib

from loguru import logger
from pymongo.errors import DuplicateKeyError, OperationFailure

from estoque_ms.api.estoque.models import StockItemDAO
from estoque_ms.api.utils import get_collection


def create_indexes():
    stock_item_collection = get_collection(StockItemDAO.collection_name())
    with contextlib.suppress(DuplicateKeyError, OperationFailure):
        stock_item_collection.create_indexes(StockItemDAO.indexes())
    logger.info("Indexes created for StockItemDAO")


def init_app() -> None:
    create_indexes()
    logger.info("DB initialized for MS de Estoque")
