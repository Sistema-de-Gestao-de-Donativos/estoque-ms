from typing import List

from fastapi import APIRouter

from . import controller, models, schemas

router = APIRouter(prefix="/stock", tags=["MS de Estoque"])


@router.get("/{codCd}", status_code=200, response_model=List[models.StockItemDAO])
def get_estoque_atual_cd(codCd: int) -> List[models.StockItemDAO]:
    return controller.get_estoque_atual_cd(codCd)


@router.post("/{codCd}", status_code=201, response_model=models.StockItemDAO)
def entrada_estoque_cd(codCd: int, input_item: list[schemas.InputStockItem]):
    items = []
    for item in input_item:
        items.append(models.StockItemDAO(codCd=codCd, **item.model_dump()))

    controller.entrada_estoque_cd(codCd, items)
    return items


@router.delete("/{codCd}", status_code=204)
def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    controller.saida_estoque_cd(codCd, codBarras, qtd)


@router.get("/{codCd}/{codBarras}", status_code=200)
def get_qtd_item_cd(codCd: int, codBarras: str) -> int:
    return controller.get_qtd_item_cd(codCd, codBarras)
