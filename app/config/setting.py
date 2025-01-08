import os
from alibabacloud_mse20190531.client import Client as mse20190531Client
from alibabacloud_credentials.client import Client as CredClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_mse20190531 import models as mse_20190531_models
from alibabacloud_tea_util import models as util_models

from typing import Type, Tuple, List
from pydantic import computed_field
from pydantic_settings import (
    BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource,
)

from app.items.app_item import App, Redis, OSS
from app.items.bot_item import Bots
from app.items.osp_item import Osp
from app.items.customer_item import Customer
from app.items.quests_item import Quests
from app.items.ufool_item import UFool
from app.utils.object_util import camel_to_snake


class Settings(BaseSettings):
    """
    系统配置参数入口
    """
    
    # bot webhook key
    OSP_COMMON_PERSONAL_WEBHOOK: str = "/bot/receiveOspCommonPersonalBotMsg"
    OSP_SPACE_GROUP_WEBHOOK: str = "/bot/receiveOspSpaceGroupBotMsg"
    UFOOL_COMMON_UFOOL_WEBHOOK: str = "/bot/receiveUFoolCommonUFoolBotMsg"
    
    # osp api
    BIND: str = "bind"
    JOIN_CHAT_GROUP: str = "bind/join/chat/group"
    CHAT_GROUP_JOIN_VERIFY: str = "chatgroup/join_verify"
    UNBIND: str = "chatgroup/unbind"
    
    # customer api
    OPEN_AUTH: str = "/customer/open/auth/{}"
    
    # quests api
    JOIN_TG_URL: str = "/v2/tasks/doquests"
    JOIN_TG_TASK_ID: str = "408011"
    
    # ufool /start 配置
    UFOOL_X: str = "https://x.com/Ufoolxyz"
    UFOOL_WELCOME_IMAGE: str = "ufool/images/tgWelcomeLogo.png"
    
    app: App  # 项目配置
    bot: Bots  # 机器人配置
    redis: Redis
    oss: OSS
    osp: Osp
    ufool: UFool
    customer: Customer
    quests: Quests
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def ufool_token(self) -> str:
        """
        get ufool bot token
        :return:
        """
        for bot in self.bot.ufool.common:
            if bot.name == 'ufool':
                return bot.token
        raise AttributeError('ufool token not exists')
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        """
        获取服务的host
        :return:
        """
        if self.app.env == "local":
            return f"http://localhost"
        return f"https://{self.app.domain}"
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def log_file_name(self) -> str:
        """
        处理日志文件名
        :return:
        """
        return camel_to_snake(self.app.name)
    
    model_config = SettingsConfigDict(yaml_file='app/config/config.yaml')
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        if os.environ.get("MSE_INSTANCE_ID") and os.environ.get("MSE_GROUP_DATA_ID") and os.environ.get(
            "MSE_NAMESPACE_ID"):
            Settings.get_mse_config()
        return (YamlConfigSettingsSource(settings_cls),)
    
    @staticmethod
    def get_mse_config():
        """
            从mse中读取对应配置信息
        :return:
        """
        try:
            config = open_api_models.Config(
                credential=CredClient()
            )
            # Endpoint 请参考 https://api.aliyun.com/product/mse
            config.endpoint = os.environ['MSE_ENDPOINT']
            client = mse20190531Client(config)
            
            get_nacos_config_request = mse_20190531_models.GetNacosConfigRequest(
                instance_id=os.environ['MSE_INSTANCE_ID'],
                data_id=os.environ['MSE_GROUP_DATA_ID'],
                group=os.environ['MSE_GROUP_DATA_ID'],
                namespace_id=os.environ['MSE_NAMESPACE_ID']
            )
            runtime = util_models.RuntimeOptions()
            
            res = client.get_nacos_config_with_options(get_nacos_config_request, runtime)
            
            with open("app/config/config.yaml", "w") as r:
                r.write(res.body.configuration.content)
        except Exception as e:
            raise e


settings = Settings()
