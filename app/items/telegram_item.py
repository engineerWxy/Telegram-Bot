from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.items.response_item import CommonResponse


class StarsPayRequest(BaseModel):
    """
    StarsPay request
    """
    title: str = Field(..., description="Product Title")
    description: str = Field(..., description="Product Description")
    image: str = Field(None, description="Product Image")
    label: str = Field(..., description="Product Label")
    amount: int = Field(..., description="Stars Amount")
    transaction_id: str = Field(None, description="Transaction Id")


class StarsPayItem(BaseModel):
    """
    StarsPay item
    """
    link: str = Field(..., description="Telegram Stars Pay Link")


class StarsPayResponse(CommonResponse):
    """
    StarsPay response
    """
    data: StarsPayItem = Field(None, description="Telegram Stars Pay Link")


class VerifyItem(BaseModel):
    """
    Telegram Verify Item
    """
    is_boost: bool | None = Field(None, description="Verify Boosts Result")
    is_premium: bool | None = Field(None, description="Verify Premium  Result")


class VerifyResponse(CommonResponse):
    """
    StarsPay response
    """
    data: VerifyItem = Field(None, description="Telegram Stars Pay Link")


class ChannelSendRequest(BaseModel):
    """
    ChannelSend Request
    """
    sass_id: str = Field(..., description="Sass ID")
    channel_name: str = Field(None, description="channel link")
    photo: Optional[str] = Field(None, description="photo url")
    message: str = Field(..., description="send message")
    inline_keyboard: List[List[Dict[str, str]]] = Field([], description="inline keyboard for the message")


class BanChatMemberRequest(BaseModel):
    """
    BanChatMember Request
    """
    sass_id: str = Field(..., description="Sass ID")
    ban_type: str = Field(..., description="ban type")
    chat_id: int = Field(..., description="chat id")
    chat_title: str = Field(None, description="chat title")
    user_id: int = Field(..., description="user id")


class LeaveChatRequest(BaseModel):
    """
    LeaveChat Request
    """
    sass_id: str = Field(..., description="Sass ID")
    chat_id: int = Field(..., description="chat id")
    chat_title: str = Field(None, description="chat title")


class VerifyGroupLinkRequest(BaseModel):
    """
    LeaveChat Request
    """
    group_type: str = Field(..., description="group type")
    group_link: str = Field(..., description="group link")
