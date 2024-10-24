from typing import List

from fastapi import APIRouter

from . import controller, models, schemas

router = APIRouter(prefix="/stock", tags=["MS de Estoque"])


@router.get("/{codCd}", status_code=200, response_model=List[models.StockItemDAO])
def get_estoque_atual_cd(codCd: int) -> List[models.StockItemDAO]:
    return controller.get_estoque_atual_cd(codCd)


@router.post("/{codCd}", status_code=201, response_model=List[models.StockItemDAO])
def entrada_estoque_cd(codCd: int, input_item: list[schemas.InputStockItem]):
    items = [
        models.StockItemDAO(codCd=codCd, **item.model_dump()) for item in input_item
    ]

    return controller.entrada_estoque_cd(codCd, items)


@router.delete("/{codCd}", status_code=204)
def saida_estoque_cd(codCd: int, codBarras: str, qtd: int) -> None:
    controller.saida_estoque_cd(codCd, codBarras, qtd)


@router.get("/{codCd}/{nome}", status_code=200)
def get_item_cd(codCd: int, nome: str) -> List[models.StockItemDAO]:
    return controller.get_item_cd(codCd, nome)
