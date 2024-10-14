from app.init_app import app
from app.routers import routers

# 初始化配置路由
app.include_router(routers)


if __name__ == '__main__':
    import uvicorn as uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=True)
