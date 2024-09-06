from typing import List
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from rapidocr_onnxruntime import RapidOCR

class RapidOCRLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def pictext(filepath):
            resp = ""
            ocr = RapidOCR()
            result, _ = ocr(filepath)
            if result:
                ocr_result = [line[1] for line in result]
                resp += "\n".join(ocr_result)
            return resp

        # 提取图像中的文本
        text = pictext(self.file_path)
        text = text.replace('\n', ' ')  # 去除换行符

        # 对提取的文本进行分割处理
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRLoader(file_path=r"...")  #将...改为文件绝对路径  #.jpg, .png均可
    docs = loader.load()
    print(docs)
