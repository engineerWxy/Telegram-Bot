import grpc.aio
from grpc_reflection.v1alpha import reflection

from facade import chat_pb2_grpc
from facade import verify_group_link_pb2_grpc
from app.services.chat_grpc_service import ChatServicer
from app.services.verify_group_link_grpc_service import VerifyLinkServicer


def chat_grpc_routes(server: grpc.aio.Server):
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)


def verify_link_grpc_routers(server: grpc.aio.Server):
    verify_group_link_pb2_grpc.add_VerifyLinkServicer_to_server(VerifyLinkServicer(), server)

#
# def chat_grpc_reflection(server: grpc.aio.Server):
#     SERVICE_NAMES = (
#         chat_pb2.DESCRIPTOR.services_by_name['Chat'].full_name,
#         reflection.SERVICE_NAME,
#     )
#     reflection.enable_server_reflection(SERVICE_NAMES, server)
