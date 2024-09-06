import sys
from new_ver.backup.configs.model_config import llm_device

# httpx_default_timeout = 60
# open_cross_domain = True
default_bind_host = '0.0.0.0' if sys.platform != 'win32' else '127.0.0.1'

webui_server = {
    "host": default_bind_host,
    "port": 8501,
}

api_server = {
    "host": default_bind_host,
    "port": 7861,
}

fastchat_openai_api = {
    "host": default_bind_host,
    "port": 20000,
}

fastchat_workers = {
    'default' : {
        'host': default_bind_host,
        'port': 20002,
        'device' : llm_device,
        'inferturbo' : False
    }
}

fastchat_multi_workers = {}

fastchat_controller = {
    'host': default_bind_host,
    'port': 20001,
    'dispatch_method' : 'shortest_queue'
}