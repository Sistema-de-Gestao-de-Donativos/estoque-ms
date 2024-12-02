from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StockItem(BaseModel):
    codCd: int = Field(..., description="Código do CD que está recebendo os itens.")
    nome: str = Field(..., description="CPF/CNPJ do doador dos itens.")
    quantidade: int = Field(..., description="Quantidade ainda disponível no estoque.")
    unidade: str = Field(..., description="Unidade de medida do item.")
    categoria: str = Field(..., description="Categoria do item.")


class InputStockItem(BaseModel):
    nome: str = Field(..., description="CPF/CNPJ do doador dos itens.")
    quantidade: int = Field(..., description="Quantidade ainda disponível no estoque.")
    unidade: str = Field(..., description="Unidade de medida do item.")
    categoria: str = Field(..., description="Categoria do item.")
