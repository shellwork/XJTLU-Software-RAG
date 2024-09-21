from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from langchain.schema import Document
import markdown
import os

# 导入 pdfminer 的高层 API
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

class PDFTextLoader:
    """
    加载 PDF 文档并将其转换为 Markdown 格式，同时使用并发处理提升速度。
    """

    def __init__(self, pdf_paths: List[str], max_workers: int = None):
        """
        初始化 PDFTextLoader。

        :param pdf_paths: 需要处理的 PDF 文件路径列表。
        :param max_workers: 并发处理的最大线程数。默认为 CPU 核心数。
        """
        self.pdf_paths = pdf_paths
        self.max_workers = max_workers or (os.cpu_count() or 4)

    def get_num_pages(self, pdf_path: str) -> int:
        """
        获取 PDF 文件的总页数。

        :param pdf_path: PDF 文件路径。
        :return: 页数。
        """
        try:
            # 使用 pdfminer 的 extract_text 仅获取总页数
            text = extract_text(pdf_path)
            # 简单估计页数，通过统计换页符（假设每页以换页符结尾）
            # 这不是精确的方法，但可以作为一个快速估计
            num_pages = text.count('\f')
            return num_pages if num_pages > 0 else 1  # 至少一页
        except (PDFSyntaxError, Exception) as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return 0

    def process_page(self, pdf_path: str, page_number: int) -> Document:
        """
        处理单个 PDF 页，提取文本并转换为 Markdown。

        :param pdf_path: PDF 文件路径。
        :param page_number: 页码（从1开始）。
        :return: Document 对象或 None。
        """
        try:
            # 使用 pdfminer 的 extract_text 仅提取指定页的文本
            # pdfminer 的 page_numbers 从0开始
            text = extract_text(pdf_path, page_numbers=[page_number - 1])
            if text:
                md_content = self._text_to_markdown(text)
                metadata = {
                    "page": page_number,
                    "source": os.path.basename(pdf_path)
                }
                return Document(page_content=md_content, metadata=metadata)
            else:
                return None
        except Exception as e:
            print(f"Error processing page {page_number} of {pdf_path}: {e}")
            return None

    def _text_to_markdown(self, text: str) -> str:
        """
        将纯文本转换为 Markdown 格式。

        :param text: 纯文本内容。
        :return: Markdown 格式的文本。
        """
        # 这里简单地返回文本转换为 Markdown，您可以根据需要增强此功能
        return markdown.markdown(text)

    def load(self) -> List[Document]:
        """
        加载并处理所有 PDF 文件，返回 Document 对象列表。

        :return: Document 对象列表。
        """
        documents = []
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for pdf_path in self.pdf_paths:
                    num_pages = self.get_num_pages(pdf_path)
                    if num_pages == 0:
                        continue  # 跳过无法读取的 PDF
                    for page_num in range(1, num_pages + 1):
                        futures[executor.submit(self.process_page, pdf_path, page_num)] = (pdf_path, page_num)

                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing PDFs"):
                    doc = future.result()
                    if doc:
                        documents.append(doc)
        except Exception as e:
            print(f"Error in concurrent loading: {e}")
        return documents
