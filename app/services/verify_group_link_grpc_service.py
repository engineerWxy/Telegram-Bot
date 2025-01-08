import time
import json
import requests
from google.protobuf.json_format import MessageToDict

import facade.verify_group_link_pb2 as pb2
import facade.verify_group_link_pb2_grpc as pb2_grpc
import facade.base_pb2 as base_pb2

from app.core.logger_handler import Log
from app.core.redis_handler import redis_handler
from app.core.grpc_error_decorator import error_handling_decorator
from app.core.error_handler import VerifyGroupLinkError, ValidateParamsError
from app.utils.enum_util import GroupType, SaasID

logger = Log()


class VerifyLinkServicer(pb2_grpc.VerifyLinkServicer):
    @error_handling_decorator
    async def verifyGroupLink(self, verify_group_link_item: pb2.VerifyGroupLinkRequest, context):
        logger.info(
            f"verify_group_link_item: {MessageToDict(verify_group_link_item, always_print_fields_with_no_presence=True)}")
        if verify_group_link_item.sassId != SaasID.SPACE.value:
            raise ValidateParamsError(f"params error")
        group_link = verify_group_link_item.groupLink
        if verify_group_link_item.groupType == GroupType.Private.value:
            group_data = redis_handler.get_object(group_link)
            logger.info(f"redis group data:{group_data}")
            if group_data:
                if not redis_handler.delete_object(group_link):
                    logger.error(f"redis delete:{verify_group_link_item.groupLink} failed, please check")
                return base_pb2.CommonResponse(code='0000', data=json.dumps(group_data))
            raise VerifyGroupLinkError(error_msg="no tg link information")
        else:
            try:
                group_link_name = group_link.split("t.me/")[-1]
                res = requests.get(verify_group_link_item.groupLink, timeout=30)
                if res.status_code == 200 and ("View in Telegram" in res.text or "Join Group" in res.text):
                    group_data = {
                        "title": group_link_name, "group_id": group_link_name, "type": GroupType.Public.value,
                        "invite_link": group_link, "created": int(time.time())
                    }
                    return base_pb2.CommonResponse(code='0000', data=json.dumps(group_data))
                msg = f"tg link does not exist: {group_link}"
                logger.error(msg)
                raise VerifyGroupLinkError(msg)
            except VerifyGroupLinkError:
                raise
            except Exception as e:
                logger.error(str(e))
                raise VerifyGroupLinkError(error_msg="tg link is invalid")
