import contextlib

from loguru import logger
from pymongo.errors import DuplicateKeyError, OperationFailure

from estoque_ms.api.estoque.models import DonorDAO, StockItemDAO, StockItemMetaDAO
from estoque_ms.api.utils import get_collection


def create_indexes():
    stock_item_collection = get_collection(StockItemDAO.collection_name())
    with contextlib.suppress(DuplicateKeyError, OperationFailure):
        stock_item_collection.create_indexes(StockItemDAO.indexes())
    logger.info("Indexes created for StockItemDAO")

    stock_item_meta_collection = get_collection(StockItemMetaDAO.collection_name())
    with contextlib.suppress(DuplicateKeyError, OperationFailure):
        stock_item_meta_collection.create_indexes(StockItemMetaDAO.indexes())
    logger.info("Indexes created for StockItemMetaDAO")

    donor_collection = get_collection(DonorDAO.collection_name())
    with contextlib.suppress(DuplicateKeyError, OperationFailure):
        donor_collection.create_indexes(DonorDAO.indexes())
    logger.info("Indexes created for DonorDAO")


def init_app() -> None:
    create_indexes()
    logger.info("DB initialized for MS de Estoque")
