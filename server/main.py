import asyncio
import grpc
from backend import StoreAPI_pb2_grpc
from backend import StoreAPI_pb2
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from uuid import uuid4
from datetime import datetime

orders = dict()


class StoreServiceServicer(StoreAPI_pb2_grpc.StoreServiceServicer):
    async def orderCreate(self, request, context):
        order = StoreAPI_pb2.Order(
            orderId=str(uuid4()),
            orderVer=1,
            status=StoreAPI_pb2.OrderStatus.DRAFT,
            createdAt=datetime.now(),
            phone=request.order.phone,
            deliveryAddress=request.order.deliveryAddress,
            items=request.order.items,
        )
        orders[order.orderId] = order
        return order

    async def orderDelete(self, request, context):
        del orders[request.orderId]
        return empty_pb2.Empty()

    async def orderList(self, request, context):
        items = list(orders.values())
        if request.orderId:
            items = [order for order in items if order.orderId == request.orderId]
        if request.status:
            items = [order for order in items if order.status == request.status]
        items.sort(key=lambda order: order.orderId)

        if request.cursor:
            for index, order in enumerate(items):
                if int(order.orderId) >= int(request.cursor):
                    items = items[index + 1 :]
                    break

        page_size = int(request.limit or 100)
        page = items[:page_size]
        next_cursor = page[-1].orderId if len(items) > page_size else None
        return StoreAPI_pb2.OrderList(cursor=next_cursor, items=page)


async def main():
    server = grpc.aio.server()
    with open("localhost.key", "rb") as f:
        key = f.read()
    with open("localhost.crt", "rb") as f:
        crt = f.read()
    credentials = grpc.ssl_server_credentials([(key, crt)])
    server.add_secure_port("0.0.0.0:50051", credentials)
    StoreAPI_pb2_grpc.add_StoreServiceServicer_to_server(StoreServiceServicer(), server)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main())
