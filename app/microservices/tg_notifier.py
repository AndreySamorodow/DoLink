from faststream.rabbit.fastapi import RabbitRouter

router = RabbitRouter(prefix="/api/tgnotify", tags=["tgnotify"])

@router.post("/order")
async def make_order(name: str):
    await router.broker.publish(
        f"Новый заказ:{name}",
        queue="orders",

    )
    return {"data": "OK"}