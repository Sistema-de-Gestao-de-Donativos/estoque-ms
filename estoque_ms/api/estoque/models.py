from datetime import datetime

from bson import ObjectId
from pydantic import Field
from pymongo import IndexModel

from . import schemas


class UserDAO(schemas.User):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def collection_name(cls) -> str:
        return "users"

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return [
            IndexModel("name", unique=True),
            IndexModel("cpf", unique=True),
            IndexModel("codEntidade"),
        ]


class StockItemDAO(schemas.StockItem):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def collection_name(cls) -> str:
        return "stock_items"

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return [
            IndexModel("nomeItem"),
            IndexModel("unidadeDeMedida"),
        ]


class StockItemMetaDAO(schemas.StockItemMeta):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def collection_name(cls) -> str:
        return "stock_item_meta"

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return [
            IndexModel("codDoador"),
            IndexModel("codCd"),
        ]


class DonorDAO(schemas.Donor):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def collection_name(cls) -> str:
        return "donors"

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return [
            IndexModel("name"),
            IndexModel("codCadastro", unique=True),
        ]
