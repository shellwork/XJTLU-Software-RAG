from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import openai
from dotenv import load_dotenv
import ollama
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


def load_api():
    load_dotenv()

    # 加载 API 密钥
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # 验证 API 密钥是否已加载
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    logging.debug("OpenAI API key loaded successfully.")


def get_model(model_name: str = "gpt-3.5-turbo", provider: str = "openai", local: bool = False, **kwargs):
    """
    根据给定的模型名称和提供商返回相应的生成模型实例。

    Args:
        local: 判断是否需要调用本地模型
        model_name (str): 要使用的模型的名称，默认使用 "gpt-3.5-turbo"。
        provider (str): 模型提供商，可以是 "openai", "cohere", "anthropic" 或 "local"。
        **kwargs: 其他可选参数，用于配置 OpenAI 模型的详细参数。

    Returns:
        model: 生成模型实例。
    """
    load_api()
    if local:
        get_local_model(model_name)
    else:
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
    """
    获取本地模型的推理实例。

    Args:
        model_name (str): 本地模型的名称。

    Returns:
        function: 本地生成模型实例。
    """
    # 定义模型存放的相对路径
    models_base_path = os.path.join("server", "model", "chat")

    # 检查模型名称是否在可用的模型列表中
    available_models = [name for name in os.listdir(models_base_path)
                        if os.path.isdir(os.path.join(models_base_path, name))]

    if model_name in available_models:
        # 在 ollama 中，模型名称通常与子文件夹名称一致
        try:
            # 检查模型是否已存在于 ollama 中
            existing_models = ollama.list_models()
            if model_name not in existing_models:
                logging.error(f"Ollama 中未找到模型: {model_name}")
                raise ValueError(f"Ollama 中未找到模型: {model_name}. 可用模型: {available_models}")

            logging.debug(f"已加载本地模型: {model_name} (路径: {models_base_path}/{model_name})")
        except Exception as e:
            logging.error(f"检查 Ollama 模型 {model_name} 时出错: {e}", exc_info=True)
            raise ValueError(f"无法加载模型 {model_name}: {e}")

        def run_model(prompt, context=None):
            """
            使用本地模型生成响应。

            Args:
                prompt (str): 用户输入的提示。
                context (str, optional): 上下文信息。

            Returns:
                str: 模型生成的响应内容。
            """
            # 组合上下文和用户输入
            if context:
                full_prompt = f"Context: {context}\n\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt

            try:
                # 使用 ollama 生成响应
                response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': full_prompt}])
                response_text = response['message']['content']
                logging.debug(f"本地模型 {model_name} 成功生成响应。")
                return response_text
            except Exception as e:
                logging.error(f"本地模型 {model_name} 生成响应时出错: {e}", exc_info=True)
                return "Error generating response from local model."

        return run_model
    else:
        raise ValueError(f"不支持的本地模型: {model_name}. 可用模型: {available_models}")


def list_available_models():
    """
    列出所有可用的本地模型。

    Returns:
        list: 模型名称列表。
    """
    models_base_path = os.path.join("server", "model", "chat")
    if not os.path.exists(models_base_path):
        logging.error(f"模型基础路径不存在: {models_base_path}")
        return []

    available_models = [name for name in os.listdir(models_base_path)
                        if os.path.isdir(os.path.join(models_base_path, name))]
    logging.debug(f"可用的本地模型: {available_models}")
    return available_models


def get_embedding_function(embed_model: str = "openai"):
    """
    根据传入的嵌入模型名称选择对应的嵌入模型。

    Args:
        embed_model (str): 嵌入模型名称，可以是 "openai"等在线模型， 或 "local"。

    Returns:
        embedding_model: 嵌入模型实例。
    """
    load_api()
    if embed_model == "openai":
        logging.debug("Using OpenAI embeddings.")
        return OpenAIEmbeddings()
    elif embed_model == "local":
        logging.debug("Using local embedding function.")
        return get_local_embedding_function()
    else:
        raise ValueError(f"Unsupported embedding model: {embed_model}")


def get_local_embedding_function(model_name: str = "all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    """
    本地嵌入模型的实现，使用 SentenceTransformer 生成文本嵌入。

    Args:
        model_name (str): 使用的 SentenceTransformer 模型名称。

    Returns:
        function: 一个生成嵌入的函数。
    """
    try:
        model = SentenceTransformer(model_name)
        logging.debug(f"Loaded local embedding model: {model_name}")
    except Exception as e:
        logging.error(f"加载本地嵌入模型 {model_name} 时出错: {e}", exc_info=True)
        raise e

    def embed(texts):
        """
        生成给定文本列表的嵌入。

        Args:
            texts (List[str]): 文本列表。

        Returns:
            np.ndarray: 嵌入向量。
        """
        try:
            embeddings = model.encode(texts, convert_to_numpy=True)
            logging.debug(f"Generated embeddings for {len(texts)} texts.")
            return embeddings
        except Exception as e:
            logging.error(f"生成嵌入时出错: {e}", exc_info=True)
            return []

    return embed
