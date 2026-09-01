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
        request = StoreAPI_pb2.EchoRequest(s="abc", n=123)
        reply = await stub.get_echo(request)
        print(reply.s)
    except Exception as e:
        print(e)
    finally:
        if channel is not None:
            await channel.close()


if __name__ == "__main__":
    asyncio.run(main())
