from pydantic import BaseModel, Field


class User(BaseModel):
    customer_id: str = Field(..., description="用户id", title='success')


class Customer(BaseModel):
    domain: str = Field(..., description="用户服务域名")
