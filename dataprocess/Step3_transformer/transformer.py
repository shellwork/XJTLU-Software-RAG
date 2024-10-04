from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json
import time
from openai import OpenAI
import sys
import threading

# Set file paths and model parameters
folder_path = '../Data'  # Input folder path
output_folder_path = '../Dataset'  # Output folder path
model = 'qwen-turbo'

client = OpenAI(
    api_key='',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def log(message):
    """Function to output log messages."""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def ensure_output_folder_exists(output_folder_path):
    """Ensure the output folder exists."""
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)


def read_txt_file(file_path):
    """Read a single .txt file and clean its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().replace('\n', ' ')
    except Exception as e:
        log(f"Error reading {file_path}: {e}")
        return ""


def split_text(text, max_tokens=7500):
    """Split text into multiple parts to meet the API's token limit."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + 1 > max_tokens:  # Consider spaces
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length + 1
        else:
            current_chunk.append(word)
            current_length += word_length + 1

    if current_chunk:  # Add the remaining part
        chunks.append(" ".join(current_chunk))

    return chunks


def extract_valid_json(text):
    """Extract valid JSON objects from a text response."""
    json_objects = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        try:
            obj, pos = decoder.raw_decode(text, pos)
            if isinstance(obj, dict):
                json_objects.append(obj)
        except json.JSONDecodeError:
            pos += 1  # Skip invalid parts
    return json_objects


def validate_and_clean_json(data):
    """Validate and clean JSON objects."""
    valid_data = []
    for item in data:
        if (
                isinstance(item, dict) and
                "instruction" in item and
                "input" in item and
                "output" in item and
                isinstance(item["instruction"], str) and
                isinstance(item["input"], str) and
                isinstance(item["output"], str)
        ):
            valid_data.append(item)
    return valid_data


class RateLimiter:
    """A simple rate limiter to ensure we don't exceed API rate limits."""

    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.lock = threading.Lock()
        self.calls = []

    def acquire(self):
        with self.lock:
            current = time.time()
            # Remove calls that are outside the current period
            while self.calls and self.calls[0] <= current - self.period:
                self.calls.pop(0)
            if len(self.calls) < self.max_calls:
                self.calls.append(current)
                return
            else:
                sleep_time = self.period - (current - self.calls[0])
        time.sleep(sleep_time)
        self.acquire()


# Initialize rate limiter: 500 requests per 60 seconds
rate_limiter = RateLimiter(max_calls=500, period=60)


def generate_qa_pairs(filename, text, max_retries=3, backoff_factor=2):
    """Generate Q&A pairs for a given file's text content with retry mechanism."""
    text_chunks = split_text(text)
    all_qa_pairs = []

    for i, chunk in enumerate(text_chunks):
        for attempt in range(1, max_retries + 1):
            try:
                rate_limiter.acquire()  # Ensure rate limiting
                log(f"Processing part {i + 1}/{len(text_chunks)} of {filename} (Attempt {attempt})...")
                prompt = f"""
                Answer in English. Based on the synthetic biology document provided by the user, generate question-answer pairs for training a large language model. Where possible, create at least 10 pairs, without numbering them. Each Q&A should answer a specific question based on the document. The context should be at least 3 sentences long and match the document content exactly without modification. Answers should be as detailed as possible, longer than 2 sentences. The pairs should cover as much of the document content as possible, extracting key information to create the required dataset in the following format:
                {{
                    "instruction": "User's question or prompt",
                    "input": "Context (a brief sentence, not the entire context)",
                    "output": "Model's response"
                }}
                Here is the provided document content: {chunk}
                """
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000
                )

                response_text = response.choices[0].message.content
                qa_pairs = extract_valid_json(response_text)
                all_qa_pairs.extend(validate_and_clean_json(qa_pairs))
                break  # Exit retry loop on success
            except Exception as e:
                log(f"Error processing part {i + 1}/{len(text_chunks)} of {filename} on attempt {attempt}: {e}")
                if attempt < max_retries:
                    sleep_time = backoff_factor ** attempt
                    log(f"Retrying after {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    log(f"Failed to process part {i + 1}/{len(text_chunks)} of {filename} after {max_retries} attempts. Skipping this part.")

    return filename, all_qa_pairs


def save_to_json(data, filename):
    """Save generated Q&A pairs to a JSON file."""
    if data:
        try:
            output_json_file = os.path.join(output_folder_path, f"{filename}.json")
            with open(output_json_file, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            log(f"Data saved to {output_json_file}")
        except Exception as e:
            log(f"Error saving data for {filename}: {e}")
    else:
        log(f"No valid Q&A pairs for {filename}, not saved.")


def process_file(file_path, max_retries=3, backoff_factor=2):
    """Process each file: check if the output already exists, if not, process and save."""
    filename = os.path.basename(file_path)
    output_file = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.json")

    # Skip processing if the output file already exists
    if os.path.exists(output_file):
        log(f"Skipping {filename}, output file already exists.")
        return

    # Read the file content
    text = read_txt_file(file_path)
    if not text:
        log(f"Skipping {filename} due to read error.")
        return

    # Generate QA pairs with retry mechanism
    try:
        filename, qa_pairs = generate_qa_pairs(filename, text, max_retries, backoff_factor)
        save_to_json(qa_pairs, os.path.splitext(filename)[0])
    except Exception as e:
        log(f"Unexpected error processing {filename}: {e}")


def main(folder_path, output_folder_path, max_workers=10):
    """Main function to process all files in the folder."""
    ensure_output_folder_exists(output_folder_path)

    # Get all .txt files in the folder
    txt_files = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if
                 file.endswith('.txt')]
    log(f"Found {len(txt_files)} .txt files to process.")

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, file): file for file in txt_files}

        # As each file is processed, log and continue
        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
                log(f"Processing of {file} completed.")
            except Exception as e:
                log(f"Error processing {file}: {e}")


if __name__ == '__main__':
    max_workers = 10  # Adjust based on your system and API rate limits
    log("Program started...")
    try:
        main(folder_path, output_folder_path, max_workers=max_workers)
    except KeyboardInterrupt:
        log("Program interrupted by user.")
        sys.exit(1)
    except Exception as e:
        log(f"Unexpected error: {e}")
        sys.exit(1)
    log("Program completed.")
