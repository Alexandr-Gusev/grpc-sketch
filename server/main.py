import asyncio
import grpc
from backend import StoreAPI_pb2_grpc
from backend import StoreAPI_pb2


class StoreServiceServicer(StoreAPI_pb2_grpc.StoreServiceServicer):
    async def get_echo(self, request, context):
        return StoreAPI_pb2.EchoReply(s=f"{request.s}{request.n}")


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
