from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import openai
from dotenv import load_dotenv

def load_api():
    load_dotenv()

    # 加载 API 密钥
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    cohere_api_key = os.environ.get('COHERE_API_KEY')
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

    # 验证 API 密钥是否已加载
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    if not cohere_api_key:
        print("Warning: COHERE_API_KEY not found in environment variables.")
    if not anthropic_api_key:
        print("Warning: ANTHROPIC_API_KEY not found in environment variables.")


def get_model(model_name: str = "gpt-3.5-turbo", provider: str = "openai", **kwargs):
    """
    根据给定的模型名称和提供商返回相应的生成模型实例。

    Args:
        model_name (str): 要使用的模型的名称，默认使用 "gpt-3.5-turbo"。
        provider (str): 模型提供商，可以是 "openai", "cohere", "anthropic" 或 "local"。
        **kwargs: 其他可选参数，用于配置 OpenAI 模型的详细参数。

    Returns:
        model: 生成模型实例。
    """
    load_api()

    if provider == "openai":
        # 配置 OpenAI 模型的详细参数
        model = ChatOpenAI(
            model_name=model_name,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
            top_p=kwargs.get("top_p", 1.0),
            frequency_penalty=kwargs.get("frequency_penalty", 0.0),
            presence_penalty=kwargs.get("presence_penalty", 0.0)
        )
        return model

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def get_local_model(model_name: str):
    import ollama
    """
    获取本地模型的推理实例。

    Args:
        model_name (str): 本地模型的名称。

    Returns:
        model: 本地生成模型实例。
    """
    if model_name.startswith("local-"):
        def run_model(prompt):
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']
        return run_model
    else:
        raise ValueError(f"Unsupported local model: {model_name}")


def get_embedding_function(provider: str = "openai"):
    """
    返回用于嵌入的模型实例。

    Args:
        provider (str): 嵌入模型提供商，可以是 "openai", "cohere" 或 "local"。

    Returns:
        embedding_model: 嵌入模型实例。
    """
    load_api()

    if provider == "openai":
        return OpenAIEmbeddings()

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def generate_response(prompt, use_local_model=False, model_name="default", tools=None):
    """
    根据用户选择的模型类型生成响应。

    Args:
        prompt (str): 用户输入的问题。
        use_local_model (bool): 是否启用本地模型推理。
        model_name (str): 要使用的模型名称。
        tools (list): 额外的工具参数。

    Returns:
        str: 模型生成的响应。
    """
    if use_local_model:
        # 使用本地模型
        model = get_local_model(model_name)
    else:
        # 使用API模型
        model = get_model(model_name)

    # 调用模型生成响应
    response = model(prompt)
    return response
