from typing import List

from fastapi import APIRouter

from . import controller, models

router = APIRouter(prefix="/stock", tags=["MS de Estoque"])


@router.get("/{codCd}", status_code=200, response_model=List[models.StockItemDAO])
def get_estoque_atual_cd(codCd: int) -> List[models.StockItemDAO]:
    return controller.get_estoque_atual_cd(codCd)


@router.post("/{codCd}", status_code=201, response_model=models.StockItemDAO)
def entrada_estoque_cd(codCd: int, body) -> models.StockItemDAO:
    return controller.entrada_estoque_cd(codCd, body)


@router.delete("/{codCd}", status_code=204)
def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    controller.saida_estoque_cd(codCd, codBarras, qtd)


# pegar a quantidade de um dado item, dado um cd
