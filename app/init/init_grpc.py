import grpc
from app.routers.grpc_routers import chat_grpc_routes, verify_link_grpc_routers
from app.core.logger_handler import Log

logger = Log()


async def start_grpc_server():
    global server
    server = grpc.aio.server()
    chat_grpc_routes(server)
    verify_link_grpc_routers(server)
    server.add_insecure_port('[::]:50051')
    logger.info("start grpc server success")
    await server.start()
    await server.wait_for_termination()


async def stop_grpc_server():
    global server
    await server.stop(grace=1)  # 等待 1 秒钟优雅关闭


server = None
