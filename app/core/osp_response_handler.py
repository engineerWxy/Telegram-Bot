from pydantic import BaseModel
from typing import Dict, List
from app.static.static import TGSendMessage
from app.utils.enum_util import OspResponseCode


class OspResponse(BaseModel):
    code: int
    msg: str | None
    data: Dict | None
    errors: List | None
    
    def get_send_message(self):
        if self.code == OspResponseCode.SUCCESS.value:
            return TGSendMessage.SUCCESS
        elif self.code == OspResponseCode.TG_CONNECTED.value:
            return TGSendMessage.TG_CONNECTED
        elif self.code == OspResponseCode.CODE_EXPIRED.value:
            return TGSendMessage.CODE_EXPIRED
        elif self.code == OspResponseCode.BUSINESS_ERROR.value:
            if isinstance(self.errors, List):
                if detail := self.errors[0].get("detail"):
                    import json
                    detail_dict = json.loads(detail)
                    if detail_dict.get("code") == OspResponseCode.OSP_CONNECTED_ANOTHER_TG.value:
                        return TGSendMessage.OSP_CONNECTED_ANOTHER_TG
        return
    
    @property
    def is_success(self):
        return self.code == OspResponseCode.SUCCESS
