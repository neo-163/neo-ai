from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from Config.modules import modules

app = FastAPI()

# 允许前端跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源,也可以设置具体的来源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 自动加载模块路由
for module_name, module_path in modules.items():
    module = __import__(module_path, fromlist=['router'])
    app.include_router(module.router)

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=1888)
