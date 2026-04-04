from fastapi import APIRouter

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

pedidos = []

@router.post("/")
def crear_pedido(pedido: dict):
    pedidos.append(pedido)
    return {"mensaje": "Pedido guardado"}