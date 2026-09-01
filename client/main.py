import asyncio
import grpc
from backend import StoreAPI_pb2_grpc
from backend import StoreAPI_pb2


async def main():
    channel = None
    try:
        with open("localhost.crt", "rb") as f:
            crt = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates=crt)
        channel = grpc.aio.secure_channel("localhost:50051", credentials)
        stub = StoreAPI_pb2_grpc.StoreServiceStub(channel)

        request = StoreAPI_pb2.OrderCreateRequest(
            idempotencyKey="demo-1",
            order=StoreAPI_pb2.OrderCreate(
                phone="123",
                deliveryAddress="456",
                items=[StoreAPI_pb2.OrderItem(
                    id="1",
                    count=1
                )]
            )
        )
        reply = await stub.orderCreate(request=request)
        print("orderCreate:", reply)
        orderId = reply.orderId

        request = StoreAPI_pb2.OrderListRequest()
        reply = await stub.orderList(request=request)
        print("orderList:", reply)

        request = StoreAPI_pb2.OrderDeleteRequest(orderId=orderId)
        reply = await stub.orderDelete(request=request)
        print("orderDelete:", reply)

        request = StoreAPI_pb2.OrderListRequest()
        reply = await stub.orderList(request=request)
        print("orderList:", reply)
    except Exception as e:
        print(e)
    finally:
        if channel is not None:
            await channel.close()


if __name__ == "__main__":
    asyncio.run(main())
