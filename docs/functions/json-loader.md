# JSON Loader
<br/>

The **`load_json_documents`** function is designed to load JSON format documents from a specified knowledge base path, processing only the files specified in the input file list. 

**Input parameters:**

· `kb_name`: The path of the knowledge base.

· `files`: The names of the files to be loaded.


**Return value:**

The function returns a list containing all the loaded documents, with each document being a `Document` object.

<br/>

```python
def load_json_documents(kb_name: str, files: list[str]) -> list[Document]:
    """
    Load OCR documents, processing only the specified files based on the 
    provided file list.
    """
    json_documents = []
    base_path = Path(kb_name)
    file_set = set(files)

    # Looking for the.json file through iterating all the subdirectories and files in the data folder
    for json_file in base_path.rglob("*.json"):
        if json_file.name in file_set:  
            print(f"Loading JSON document: {json_file}")
            with open(json_file, "r", encoding="utf-8") as file:
                json_data = json.load(file)

                # If json_data is a list, iterate through each item
                if isinstance(json_data, list):
                    for entry in json_data:
                        document_id = entry.get("document_id", Path(json_file).stem)
                        content = json.dumps(entry, indent=2)  # Store the entire entry as text

                        # Process a list-type metadata field, converting it to a comma-separated string
                        tags = entry.get("tags", [])
                        if isinstance(tags, list):
                            tags = ", ".join(tags)  # Convert to a comma-separated string

                        # Process metadata fields of dictionary type, converting them to strings
                        metadata_dict = entry.get("metadata", {})
                        if isinstance(metadata_dict, dict):
                            metadata_str = "; ".join([f"{k}: {v}" for k, v in metadata_dict.items()])

                        metadata = {
                            "document_id": document_id,
                            "title": entry.get("title", "Untitled"),
                            "author": entry.get("author", "Unknown"),
                            "date": entry.get("date", "Unknown"),
                            "tags": tags,
                            "abstract": entry.get("abstract", ""),
                            "metadata": metadata_str,  # Store as string
                            "url": entry.get("url", ""),
                            "source": str(json_file)
                        }
                        json_document = Document(page_content=content, metadata=metadata)
                        json_documents.append(json_document)
                else:
                    print(f"Unexpected JSON structure in {json_file}, skipping...")

    print(f"Loaded {len(json_documents)} JSON documents.")
    return json_documents
```