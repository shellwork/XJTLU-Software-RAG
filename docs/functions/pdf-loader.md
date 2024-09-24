# PDF Loader
<br/>

The **`RapidOCRPDFLoader`** class extends `UnstructuredFileLoader` and is designed to load and process PDF files using Optical Character Recognition (OCR). 

**Input parameters:**

`file_path`: The path of the PDF file to be loaded.

**Methods:**

`_get_elements`: Extracts text and images from the PDF using OCR. It iterates through each page, retrieves text, processes images with OCR, and returns the structured text.

`pdftext`(nested function): Handles the actual text extraction and OCR processing for each page of the PDF.

**Return value:**

Returns a list of structured text documents after processing the PDF.

```python
class RapidOCRPDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def pdftext(filepath):

            ocr = RapidOCR()
            doc = fitz.open(filepath)
            expt = ""

            unit = tqdm.tqdm(total=doc.page_count, desc="RapidOCRPDFLoader context page index: 0")
            for i, page in enumerate(doc):

                unit.set_description("RapidOCRPDFLoader context page index: {}".format(i))
                # Immediatly display progress bar update results
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

                # update progress
                unit.update(1)
            return expt

        text = pdftext(self.file_path)
        text = text.replace('\n', ' ')  # Remove the line breaks
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRPDFLoader(file_path=r"...")  # Change ... to the absolute path of the file
    docs = loader.load()
    print(docs)
```