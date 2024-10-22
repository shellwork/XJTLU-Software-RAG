from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
import openai
from dotenv import load_dotenv
import ollama
import logging
import dashscope
from http import HTTPStatus
from typing import Callable, List, Dict
from langchain.embeddings.base import Embeddings
import sys
from pathlib import Path

folder = Path(__file__).resolve().parents[2]
sys.path.append(str(folder))
from config import LOCAL_MODEL_DIR

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 自定义qwen类
import logging
from typing import List
from langchain.embeddings.base import Embeddings
from http import HTTPStatus
import dashscope
import numpy as np


class QwenEmbeddings(Embeddings):
    def __init__(self, model_version: str = "text-embedding-async-v2"):
        supported_models = [
            "text-embedding-v1",
            "text-embedding-async-v1",
            "text-embedding-v2",
            "text-embedding-async-v2",
            "text-embedding-v3"
        ]

        if model_version not in supported_models:
            raise ValueError(f"不支持的 Qwen 嵌入模型版本: {model_version}. 支持的版本: {supported_models}")

        self.model_version = model_version

    def normalize_embedding(self, embedding: List[float]) -> List[float]:
        norm = np.linalg.norm(embedding)
        if norm == 0:
            logging.warning("Embedding norm is zero. Returning the original embedding.")
            return embedding
        return (np.array(embedding) / norm).tolist()

    def is_valid_embedding(self, embedding: List[float]) -> bool:
        return all(np.isfinite(val) for val in embedding)

    def embed_query(self, text: str) -> List[float]:
        try:
            resp = dashscope.TextEmbedding.call(
                model=self.model_version,
                input=text
            )
            if resp.status_code == HTTPStatus.OK:
                embedding = resp.output['embeddings'][0].get('embedding')
                if embedding:
                    embedding = self.normalize_embedding(embedding)
                    if self.is_valid_embedding(embedding):
                        logging.debug(f"成功生成并归一化查询文本的嵌入: {text}")
                        return embedding
                    else:
                        logging.error(f"嵌入向量包含无效值: {embedding}")
                        return []
                else:
                    logging.error(f"嵌入响应中缺少嵌入向量: {resp.output}")
                    return []
            else:
                logging.error(f"嵌入请求失败。文本: {text}, 响应: {resp}")
                return []
        except Exception as e:
            logging.error(f"生成 Qwen 查询嵌入时出错: {e}", exc_info=True)
            return []

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        try:
            if "async" in self.model_version:
                logging.debug("使用异步批量嵌入。")
                resp = dashscope.TextEmbedding.call(
                    model=self.model_version,
                    input=texts
                )
                if resp.status_code == HTTPStatus.OK:
                    for item in resp.output['embeddings']:
                        embedding = item.get('embedding')
                        if embedding:
                            embedding = self.normalize_embedding(embedding)
                            if self.is_valid_embedding(embedding):
                                embeddings.append(embedding)
                            else:
                                logging.error(f"嵌入向量包含无效值: {embedding}")
                                embeddings.append([])
                        else:
                            logging.error(f"缺少嵌入向量: {item}")
                            embeddings.append([])
                else:
                    logging.error(f"批量嵌入请求失败。响应: {resp}")
                    embeddings = [[] for _ in texts]
            else:
                logging.debug("使用同步嵌入。")
                for text in texts:
                    resp = dashscope.TextEmbedding.call(
                        model=self.model_version,
                        input=text
                    )
                    if resp.status_code == HTTPStatus.OK:
                        embedding = resp.output['embeddings'][0].get('embedding')
                        if embedding:
                            embedding = self.normalize_embedding(embedding)
                            if self.is_valid_embedding(embedding):
                                embeddings.append(embedding)
                                logging.debug(f"成功生成并归一化文本的嵌入: {text}")
                            else:
                                logging.error(f"嵌入向量包含无效值: {embedding}")
                                embeddings.append([])
                        else:
                            logging.error(f"嵌入响应中缺少嵌入向量: {resp.output}")
                            embeddings.append([])
                    else:
                        logging.error(f"嵌入请求失败。文本: {text}, 响应: {resp}")
                        embeddings.append([])
            return embeddings
        except Exception as e:
            logging.error(f"生成 Qwen 文档嵌入时出错: {e}", exc_info=True)
            return [[] for _ in texts]


def load_api():
    load_dotenv()

    # 加载 OpenAI API 密钥
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    openai.api_key = openai_api_key
    logging.debug("OpenAI API key loaded successfully.")

    # 加载 Dashscope API 密钥和 Qwen Base URL
    dashscope_api_key = os.environ.get('DASHSCOPE_API_KEY')
    qwen_base_url = os.environ.get('QWEN_BASE_URL')
    if not dashscope_api_key:
        raise ValueError("DASHSCOPE_API_KEY not found in environment variables.")
    if not qwen_base_url:
        raise ValueError("QWEN_BASE_URL not found in environment variables.")
    dashscope.api_key = dashscope_api_key
    logging.debug("Dashscope API key and Qwen base URL loaded successfully.")


def get_model(model_name: str = "gpt-3.5-turbo", provider: str = "openai", local: bool = False, **kwargs):
    """
    根据给定的模型名称和提供商返回相应的生成模型实例。

    Args:
        local: 判断是否需要调用本地模型
        model_name (str): 要使用的模型的名称，默认使用 "gpt-3.5-turbo"。
        provider (str): 模型提供商，可以是 "openai", "qwen"。
        **kwargs: 其他可选参数，用于配置模型的详细参数。

    Returns:
        model: 生成模型实例。
    """
    load_api()
    if local:
        return get_local_model(model_name)
    else:
        if provider == "openai":
            # 配置 OpenAI 模型的详细参数
            model = ChatOpenAI(
                model_name=model_name,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0.0),
                presence_penalty=kwargs.get("presence_penalty", 0.0),
                openai_api_key=os.environ.get('OPENAI_API_KEY'),
                openai_api_base=kwargs.get("openai_api_base")  # 默认使用 OpenAI 的 API base
            )
            return model
        elif provider == "qwen":
            # 配置通义Qwen模型的详细参数
            model = ChatOpenAI(
                model_name=model_name,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0.0),
                presence_penalty=kwargs.get("presence_penalty", 0.0),
                openai_api_key=os.environ.get('DASHSCOPE_API_KEY'),  # 使用 Dashscope API Key
                openai_api_base=os.environ.get('QWEN_BASE_URL')  # 使用 Qwen 的 API base
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


class LocalEmbeddings(Embeddings):
    def __init__(self, model_path: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        model_full_path = os.path.join(LOCAL_MODEL_DIR, "embedding", model_path)
        try:
            if os.path.exists(model_full_path):
                logging.info(f"加载本地嵌入模型: {model_full_path}")
                self.model = SentenceTransformer(model_full_path)
            else:
                logging.info(f"加载预训练嵌入模型: {model_path}")
                self.model = SentenceTransformer(model_path)
            logging.debug(f"Loaded local embedding model: {model_full_path}")
        except Exception as e:
            logging.error(f"加载嵌入模型 {model_full_path} 时出错: {e}", exc_info=True)
            raise e

    def embed_query(self, text: str) -> List[float]:
        try:
            embedding = self.model.encode([text], convert_to_numpy=True).tolist()[0]
            logging.debug(f"Generated embedding for query: {text}")
            return embedding
        except Exception as e:
            logging.error(f"生成查询嵌入时出错: {e}", exc_info=True)
            return []

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
            logging.debug(f"Generated embeddings for {len(texts)} texts.")
            return embeddings
        except Exception as e:
            logging.error(f"生成嵌入时出错: {e}", exc_info=True)
            return [[] for _ in texts]


def get_embedding_function(embed_model: str = "", provider: str = "openai", local: bool = False) -> LocalEmbeddings:
    """
    根据传入的嵌入模型名称选择对应的嵌入模型。

    Args:
        local: 是否调用本地模型
        provider: 模型提供商
        embed_model (str): 嵌入模型名称，可以是: "openai"、"qwen"。

    Returns:
        Callable[[List[str]], List[List[float]]]: 一个生成嵌入的函数。
    """
    load_api()
    if local:
        logging.debug("Using local embedding function.")
        embedding_function = get_local_embedding_function(embed_model)
        return embedding_function  # 确保返回的是 embed_query 方法
    else:
        if provider == "openai":
            logging.debug("Using OpenAI embeddings.")
            embeddings = OpenAIEmbeddings()
            return embeddings
        elif provider == "qwen":
            logging.debug("Using Qwen embeddings.")
            embeddings = QwenEmbeddings(embed_model)
            return embeddings
        else:
            raise ValueError(f"Unsupported embedding model: {embed_model}")


def get_local_embedding_function(model_path: str = "all-MiniLM-L6-v2") -> LocalEmbeddings:
    """
    本地嵌入模型的实现，使用 SentenceTransformer 生成文本嵌入。
    """
    return LocalEmbeddings(model_path)
