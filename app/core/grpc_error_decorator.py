from app.core.logger_handler import Log
from app.core.error_handler import CommonServerError
import facade.base_pb2 as base_pb2

logger = Log()


def error_handling_decorator(func):
    async def wrapper(self, request, context):
        try:
            # 调用原始的 gRPC 服务方法
            return await func(self, request, context)
        except CommonServerError as e:
            logger.error(f"grpc common error:{e}")
            return base_pb2.CommonResponse(code=e.code, message=e.message, errorMsg=e.error_msg)
        except Exception as e:
            logger.error(f"grpc exception error:{e}")
            return base_pb2.CommonResponse(code=500, message="Internal Server Error")
    
    return wrapper
