# PDF & Text Loader
<br/>

The **`process_page`** function is designed to process a single page of a PDF file, extracting its text and converting it into Markdown format.

**Input parameters:**

· `pdf_path`: The path to the PDF file.

· `page_number`: The page number to be processed (1-based index).

**Return value:**

If the text extraction is successful, the function returns a `Document` object containing the Markdown content and the associated metadata.

If no text is extracted or an error occurs, it returns `None` and prints an error message.

```python
def process_page(self, pdf_path: str, page_number: int) -> Document:
        """
        Process a single PDF page, extract the text and convert it to Markdown.

        :param pdf_path: PDF file path
        :param page_number: page number(start from 1)
        :return: Document object or None
        """
        try:
            # Use pdfminer's extract_text to extract the text of the specified page
            # pdfminer's page numbers start at 0
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
```

<br/>

---
The **`_text_to_markdown`** function is designed to convert plain text into Markdown format.

```python
def _text_to_markdown(self, text: str) -> str:
        """
        Converts plain text to Markdown format.

        :param text: Plain text content.
        :return: Text in Markdown format.
        """
        # This simply returns the text converted to Markdown 
        # which you can enhance as needed
        return markdown.markdown(text)
```

<br/>

---
The **`load`** function is designed to load and process all specified PDF files, returning a list of `Document` objects.

**Return value:**

Returns a list of `Document` objects.

**Error handling:**

If an error arises during the concurrent loading process, an error message is displayed.

```python
def load(self) -> List[Document]:
        """
        Load and process all PDF files, returning a list of Document objects.

        :return: Document object list.
        """
        documents = []
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for pdf_path in self.pdf_paths:
                    num_pages = self.get_num_pages(pdf_path)
                    if num_pages == 0:
                        continue  # Skip unreadable PDF
                    for page_num in range(1, num_pages + 1):
                        futures[executor.submit(self.process_page, pdf_path, page_num)] = (pdf_path, page_num)

                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing PDFs"):
                    doc = future.result()
                    if doc:
                        documents.append(doc)
        except Exception as e:
            print(f"Error in concurrent loading: {e}")
        return documents
```