from datetime import datetime

from bson import ObjectId
from pydantic import Field
from pymongo import IndexModel

from . import schemas


class StockItemDAO(schemas.StockItem):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def collection_name(cls) -> str:
        return "stock_item_meta"

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return [
            IndexModel("nome"),
            IndexModel("codCd"),
        ]
