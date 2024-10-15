from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class StockItem(BaseModel):
    codCd: int = Field(
        ..., description="Código do CD que está recebendo os itens."
    )  # remover isso do objeto de entrada, isso vem no query param
    nome: str = Field(..., description="CPF/CNPJ do doador dos itens.")
    quantidade: int = Field(..., description="Quantidade ainda disponível no estoque.")
    unidade: str = Field(..., description="Unidade de medida do item.")
    dataValidade: Optional[date] = Field(None, description="Data de validade do item.")
