from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from ..utils import validate_cpf


class Adress(BaseModel):  # from user_ms
    country: str
    state: str
    city: str
    neighborhood: str
    street: str
    number: int


class User(BaseModel):  # from user_ms
    name: str
    address: Adress
    email: EmailStr
    phone: str
    role: Literal["voluntario", "adminCD", "adminAbrigo", "superadmin"]
    codEntidade: int
    cpf: str = Field(..., description="CPF (Cadastro de Pessoas Físicas)")

    @field_validator("cpf")  # from user_ms
    def cpf_validator(cls, v):
        return validate_cpf(v)


class Donor(BaseModel):
    name: str = Field(..., description="Nome completo do doador.")
    address: Adress
    email: EmailStr = Field(..., description="Email do doador.")
    phone: str = Field(..., description="Telefone do doador.")
    codCadastro: str = Field(..., description="CPF/CNPJ do doador.")


class StockItem(BaseModel):
    nomeItem: str = Field(..., description="Nome do item.")
    unidadeDeMedida: str = Field(..., description="Unidade de medida do item.")
    multiplicador: str = Field(
        ..., description="Tamanho do item relativo à unidade de medida."
    )
    tags: List[str] = Field(..., description="Tags associadas ao item.")


class StockItemMeta(BaseModel):
    codDoador: str = Field(..., description="CPF/CNPJ do doador dos itens.")
    codCd: int = Field(..., description="Código do CD que está recebendo os itens.")
    qtdDoada: int = Field(..., description="Quantidade do item que foi doada.")
    qtdAtual: int = Field(..., description="Quantidade ainda disponível no estoque.")
    dataDoacao: date = Field(
        ..., description="Data em que os itens entraram no estoque."
    )
    dataValidade: Optional[date] = Field(None, description="Data de validade do item.")


class GenericErrorMessage(BaseModel):
    message: str = Field(..., description="Informações sobre o erro.")


class Id(BaseModel):
    code: str = Field(
        ..., description="Identificador único gerado automaticamente para o objeto."
    )

    phone: str
    role: Literal["voluntario", "adminCD", "adminAbrigo", "superadmin"]
    codEntidade: int
    cpf: str = Field(..., description="CPF (Cadastro de Pessoas Físicas)")

    @field_validator("cpf")
    def cpf_validator(cls, v):
        return validate_cpf(v)
