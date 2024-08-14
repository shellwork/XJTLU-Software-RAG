from typing import List
from langchain.document_loaders.unstructured import UnstructuredFileLoader
import tqdm


class RapidOCRPDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def pdftext(filepath):
            import fitz
            from rapidocr_onnxruntime import RapidOCR
            import numpy as np
            ocr = RapidOCR()
            doc = fitz.open(filepath)
            expt = ""

            unit = tqdm.tqdm(total=doc.page_count, desc="RapidOCRPDFLoader context page index: 0")
            for i, page in enumerate(doc):

                unit.set_description("RapidOCRPDFLoader context page index: {}".format(i))
                # 立即显示进度条更新结果
                unit.refresh()

                text = page.get_text("")
                expt += text + "\n"

                img_list = page.get_images()
                for img in img_list:
                    pix = fitz.Pixmap(doc, img[0])
                    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)
                    result, _ = ocr(img_array)
                    if result:
                        ocr_result = [line[1] for line in result]
                        expt += "\n".join(ocr_result)

                # 更新进度
                unit.update(1)
            return expt

        text = pdftext(self.file_path)
        text = text.replace('\n', ' ')  # 去除换行符
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRPDFLoader(file_path=r"...")  #将...改为文件的绝对路径  #.pdf, .txt均可
    docs = loader.load()
    print(docs)
