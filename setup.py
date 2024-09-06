from setuptools import setup
import subprocess


def run_services():
    # 启动前端服务
    frontend_process = subprocess.Popen(["streamlit", "run", "webui.py"])

    # 启动后端服务
    backend_process = subprocess.Popen(["uvicorn", "api:app", "--reload"], cwd='./server')

    # 等待两个服务运行
    frontend_process.wait()
    backend_process.wait()


# 运行服务
run_services()

setup(
    name='project_name',
    version='0.1',
    description='A setup script to run frontend and backend services',
    py_modules=[],
)
