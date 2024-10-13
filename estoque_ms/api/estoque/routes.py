from typing import List, Optional

from fastapi import APIRouter

from . import controller, models, schemas

router = APIRouter(prefix="/stock", tags=["MS de Estoque"])


@router.get("/{codCd}", status_code=200, response_model=List[models.StockItemMetaDAO])
def get_estoque_atual_cd(codCd: int) -> List[models.StockItemMetaDAO]:
    return controller.get_estoque_atual_cd(codCd)


@router.post("/{codCd}", status_code=201, response_model=models.StockItemMetaDAO)
def entrada_estoque_cd(
    codCd: int, item: schemas.StockItemMeta
) -> models.StockItemMetaDAO:
    return controller.entrada_estoque_cd(codCd, item)


@router.delete("/{codCd}", status_code=204)
def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    controller.saida_estoque_cd(codCd, codBarras, qtd)


@router.get(
    "/history/{codCd}", status_code=200, response_model=List[models.StockItemMetaDAO]
)
def get_estoque_historico_cd(
    codCd: int, since: Optional[str] = None
) -> List[models.StockItemMetaDAO]:
    return controller.get_estoque_historico_cd(codCd, since)
