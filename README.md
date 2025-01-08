# tele_pulse

## Getting Started

Install dependencies and start a local dev server.

### 配置文件
static/config.yaml
* 具体参数及格式请参考static/config_demo.yaml
* 线上环境的配置采取阿里云MSE参数管理
* server-host为本服务对外公开可访问的地址，本地开发阶段可借助ngrok类似工具来映射

#### 项目依赖
* python3.7+
* platform:Mac/Linux
* package requirements.txt

### 项目启动/部署
```
pip install -r requirements.txt
uvicorn main:app
```
默认 127.0.0.1:8000，可通过--host/post指定

#### 日志采集
后续部署时再考虑接入SLS

## API-Public
http://127.0.0.1:8000/docs#/
http://127.0.0.1:8000/redoc



## 机器人
具体相关信息参考语雀调研文档
### 机器人创建
本服务将直接引用开发分析文档中的token,后续根据环境再额外创建，区别隔离
### 机器人配置
* 如果涉及群聊，需额外授予群聊中机器人的admin权限
* token验证额外需要设立两个command，辅助交互和webhook的识别捕获

## 功能说明
具体参考开发分析文档
### 玩家绑定
* OSP申请token(验证码)
* 线下进入telegram APP,通过私聊机器人（person bot），发送token
* 进而与后端达成核验、绑定的操作。

### 群聊绑定
* OSP申请token(验证码)
* 玩家进入telegram APP，创建群聊，并引入群聊机器人，配置权限
* 通过私聊机器人（group bot），发送token
* 进而与后端达成核验、群托管的操作。

### 群聊新成员身份核验
* 新用户以某种渠道进入群聊
* 系统group-webhook识别到上述事件或动作，解析玩家信息
* 与后端核验用户,不符合条件，踢出用户

