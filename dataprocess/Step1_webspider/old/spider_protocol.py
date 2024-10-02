import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
import csv

# User-configurable variables
text_folder = './data/wiki_texts'
image_folder = './data/wiki_images'

# Configuration options
download_images = False
download_texts = True

session = requests.Session()
request_timeout = 60

def safe_filename(base_filename):
    base_filename = re.sub(r'[^\w\s-]', '_', base_filename)
    ascii_filename = base_filename.encode('ascii', 'ignore').decode('ascii')
    return ascii_filename + '.txt'

def safe_print(content):
    try:
        print(content.encode('utf-8', 'replace').decode('utf-8'))
    except UnicodeEncodeError:
        print("Error printing content due to encoding issues.")

def fetch_urls_from_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            year = row['year']
            team_name = row['team']
            base_url = row['wiki']
            protocol_url = f"{base_url}/protocol"
            experiments_url = f"{base_url}/experiments"
            data.append({'year': year, 'team_name': team_name, 'protocol_url': protocol_url, 'experiments_url': experiments_url})
    return data

def process_webpage(data, text_folder):
    for entry in data:
        year = entry['year']
        team_name = entry['team_name']
        protocol_url = entry['protocol_url']
        experiments_url = entry['experiments_url']

        def fetch_and_process(url):
            try:
                safe_print(f"Processing webpage: {url}")
                response = session.get(url, timeout=request_timeout)
                if response.status_code == 404:
                    safe_print(f"Page not found: {url}")
                    return False

                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')

                filename = f"{year}_{team_name}_protocol" if "protocol" in url else f"{year}_{team_name}_experiments"
                full_text_path = os.path.join(text_folder, safe_filename(filename))
                os.makedirs(text_folder, exist_ok=True)

                if download_texts:
                    text_content = ' '.join(soup.stripped_strings)
                    with open(full_text_path, 'w', encoding='utf-8') as file:
                        file.write(text_content)
                    safe_print(f"Saved text content to: {full_text_path}")

                return True
            except requests.RequestException as e:
                safe_print(f"Error processing {url}: {e}")
                return False

        # Try to fetch and process the protocol page first, if it fails, try the experiments page
        if not fetch_and_process(protocol_url):
            fetch_and_process(experiments_url)

def process_csv_file(csv_file_path):
    safe_print(f"Processing CSV file: {csv_file_path}")
    data = fetch_urls_from_csv(csv_file_path)
    process_webpage(data, text_folder)

def main():
    csv_folder = './data/list'
    csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_csv_file, csv_file_path) for csv_file_path in csv_files]
        concurrent.futures.wait(futures)

    safe_print("All URLs and subpages fetched and processed successfully.")

if __name__ == "__main__":
    main()
