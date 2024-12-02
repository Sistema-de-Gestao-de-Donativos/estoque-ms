from typing import List

from fastapi import APIRouter, HTTPException, Request

from . import controller, models, schemas

router = APIRouter(prefix="/stock", tags=["MS de Estoque"])


@router.get("/{codCd}", status_code=200, response_model=List[models.StockItemDAO])
def get_estoque_atual_cd(request: Request, codCd: int) -> List[models.StockItemDAO]:
    allowed_roles = ["superadmin"]
    if request.state.user["role"] not in allowed_roles:
        raise HTTPException(403, detail="Unauthorized")
    return controller.get_estoque_atual_cd(codCd)


@router.post("/{codCd}", status_code=201, response_model=List[models.StockItemDAO])
def entrada_estoque_cd(
    request: Request, codCd: int, input_item: list[schemas.InputStockItem]
):
    allowed_roles = ["superadmin"]
    if request.state.user["role"] not in allowed_roles:
        raise HTTPException(403, detail="Unauthorized")
    items = [
        models.StockItemDAO(codCd=codCd, **item.model_dump(by_alias=True))
        for item in input_item
    ]

    return controller.entrada_estoque_cd(codCd, items)


@router.delete("/{codCd}", status_code=204)
def saida_estoque_cd(request: Request, codCd: int, nome: str, qtd: int) -> None:
    allowed_roles = ["superadmin"]
    if request.state.user["role"] not in allowed_roles:
        raise HTTPException(403, detail="Unauthorized")
    controller.saida_estoque_cd(codCd, nome, qtd)


@router.get("/{codCd}/{nome}", status_code=200)
def get_item_cd(request: Request, codCd: int, nome: str) -> List[models.StockItemDAO]:
    allowed_roles = ["superadmin"]
    if request.state.user["role"] not in allowed_roles:
        raise HTTPException(403, detail="Unauthorized")

    return controller.get_item_cd(codCd, nome)
