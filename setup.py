from setuptools import setup
import subprocess
import config


def run_services():
    # 输出启动信息
    print(config.project_name)
    print(config.welcome)
    print(f"Version: {config.__version__}")
    # 启动前端服务
    frontend_process = subprocess.Popen(["streamlit", "run", "webui.py", "--server.port", str(config.PORT)])

    # 启动后端服务
    backend_process = subprocess.Popen(["uvicorn", "api:app", "--reload"], cwd='./server')

    # 等待两个服务运行
    frontend_process.wait()
    backend_process.wait()


# 运行服务
run_services()

setup(
    name=config.project_name,
    version=config.__version__,
    description=config.welcome,
)