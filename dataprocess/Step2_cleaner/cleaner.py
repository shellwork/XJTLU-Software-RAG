import os
import chardet
from bs4 import BeautifulSoup


def delete_small_files(folder_path, min_size_kb=1):
    """
    Delete files in the specified folder that are smaller than the given size.
    """
    min_size_bytes = min_size_kb * 1024
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            if file_size < min_size_bytes:
                print(f"Deleting {file_path}, size: {file_size} bytes")
                os.remove(file_path)


def detect_encoding(file_path):
    """
    Detect file encoding, default to UTF-8 if not found.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding'] if result['encoding'] else 'utf-8'


def clean_text(text):
    """
    Clean the text content by removing HTML tags, non-ASCII characters, and duplicate lines.
    """
    # Remove HTML tags
    soup = BeautifulSoup(text, "lxml")
    cleaned_text = soup.get_text(separator=' ', strip=True)

    # Remove non-ASCII characters
    cleaned_text = ''.join([char if ord(char) < 128 else ' ' for char in cleaned_text])

    # Remove duplicate lines
    lines = cleaned_text.splitlines()
    cleaned_text = "\n".join(sorted(set(lines), key=lines.index))

    return cleaned_text


def clean_files(folder_path):
    """
    Clean file content by standardizing encoding, removing HTML tags, and removing non-ASCII characters.
    """
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Only process text files
            if file_name.endswith('.txt'):
                encoding = detect_encoding(file_path)

                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text = file.read()

                    cleaned_text = clean_text(text)

                    # If the cleaned text is empty, delete the file
                    if not cleaned_text.strip():
                        print(f"Deleting empty or invalid file after cleaning: {file_path}")
                        os.remove(file_path)
                    else:
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(cleaned_text)
                        print(f"Cleaned and saved file: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    # Specify the top-level folder path you want to clean
    top_level_folder = '../Data'

    # Step 1: Delete small files
    delete_small_files(top_level_folder, min_size_kb=1)

    # Step 2: Clean text files
    clean_files(top_level_folder)

    print("Cleaning completed.")
