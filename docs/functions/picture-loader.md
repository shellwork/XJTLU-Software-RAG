# Picture Loader
<br/>

The **`RapidOCRLoader`** class extends **UnstructuredFileLoader** and is designed to extract text from image files (such as .jpg and .png) using Optical Character Recognition (OCR).

**Input parameters:**

`file_path`: The absolute path of the image file to be loaded.

**Methods:**

The `pictext` function takes a file path and initializes an OCR instance (`RapidOCR`). It extracts text from the image, returning the concatenated results as a string if any text is found.

The `_get_elements` method uses the nested function `pictext` to extract text from the image file via OCR, replacing newline characters with spaces. It then processes the text with `partition_text` from the `unstructured` library for structured output.

**Return value:**

Returns a list of structured text documents after processing the image.

```python
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

        # Extract text from the image
        text = pictext(self.file_path)
        text = text.replace('\n', ' ')  # Remove the line breaks

        # The extracted text is segmented
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRLoader(file_path=r"...")  #Change ... to the absolute path of the file
    docs = loader.load()
    print(docs)
```