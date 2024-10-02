import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
import csv

# User-configurable variables
model_folder = './data/wiki_text'  # Set the output path for text files
image_folder = './data/wiki_images'  # Set the output path for image files

# Configuration options
download_images = False
download_texts = True

session = requests.Session()
request_timeout = 60

def safe_filename(base_filename):
    """
    Generates a safe filename ensuring it is ASCII compatible.
    """
    base_filename = re.sub(r'[^\w\s-]', '_', base_filename)  # Replace non-word characters with underscore
    ascii_filename = base_filename.encode('ascii', 'ignore').decode('ascii')  # Ensure ASCII compatibility
    return ascii_filename + '_model.txt'

def safe_print(content):
    """
    Safely print the content handling any encoding issues.
    """
    try:
        print(content.encode('utf-8', 'replace').decode('utf-8'))
    except UnicodeEncodeError:
        print("Error printing content due to encoding issues.")

def fetch_urls_from_csv(file_path):
    """
    Fetch URLs, year, and team names from a CSV file.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            year = row['year']
            team_name = row['team']
            url = f"{row['wiki']}/model" if not row['wiki'].endswith('/model') else row['wiki']
            data.append({'year': year, 'team_name': team_name, 'url': url})
    return data

def get_valid_subpage_urls(main_url, soup):
    """
    Get all valid subpage URLs that contain "parts.igem.org/Part:" from the main page soup object.
    """
    subpage_urls = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        full_url = urljoin(main_url, href)
        if "parts.igem.org/Part:" in full_url:
            subpage_urls.add(full_url)
    return subpage_urls

def fetch_sequence_page(parts_number):
    """
    Fetch the sequence page for a given parts number.
    """
    sequence_url = f"https://parts.igem.org/cgi/partsdb/composite_edit/putseq.cgi?part={parts_number}"
    try:
        sequence_response = session.get(sequence_url, timeout=request_timeout)
        if sequence_response.status_code == 404:
            safe_print(f"Sequence page not found: {sequence_url}")
            return None

        sequence_response.raise_for_status()
        return sequence_response.text
    except requests.RequestException as e:
        safe_print(f"Error fetching sequence page {sequence_url}: {e}")
        return None

def process_webpage(data, text_folder):
    """
    Process webpages from the list of URLs, downloading texts for each URL and its subpages.
    """
    for entry in data:
        year = entry['year']
        team_name = entry['team_name']
        main_url = entry['url']

        try:
            safe_print(f"Processing webpage: {main_url}")
            main_response = session.get(main_url, timeout=request_timeout)
            if main_response.status_code == 404:
                safe_print(f"Page not found: {main_url}")
                continue

            main_response.raise_for_status()
            main_soup = BeautifulSoup(main_response.content, 'lxml')

            # Process the main page
            filename = f"{year}_{team_name}_wiki"
            full_text_path = os.path.join(text_folder, safe_filename(filename))
            os.makedirs(text_folder, exist_ok=True)

            if download_texts:
                text_content = ' '.join(main_soup.stripped_strings)
                with open(full_text_path, 'w', encoding='utf-8') as file:
                    file.write(text_content)
                safe_print(f"Saved text content to: {full_text_path}")

            # Process subpages
            subpage_urls = get_valid_subpage_urls(main_url, main_soup)
            for sub_url in subpage_urls:
                safe_print(f"Processing subpage: {sub_url}")
                sub_response = session.get(sub_url, timeout=request_timeout)
                if sub_response.status_code == 404:
                    safe_print(f"Subpage not found: {sub_url}")
                    continue

                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.content, 'lxml')

                parts_number = urlparse(sub_url).path.split(':')[-1]
                sub_filename = f"{year}_{team_name}_{parts_number}"
                sub_full_text_path = os.path.join(text_folder, safe_filename(sub_filename))

                if download_texts:
                    sub_text_content = ' '.join(sub_soup.stripped_strings)
                    with open(sub_full_text_path, 'w', encoding='utf-8') as sub_file:
                        sub_file.write(sub_text_content)
                    safe_print(f"Saved subpage text content to: {sub_full_text_path}")

                # Fetch and save sequence page
                sequence_content = fetch_sequence_page(parts_number)
                if sequence_content:
                    sequence_filename = f"{year}_{team_name}_{parts_number}_sequence"
                    sequence_full_text_path = os.path.join(text_folder, safe_filename(sequence_filename))
                    with open(sequence_full_text_path, 'w', encoding='utf-8') as sequence_file:
                        sequence_file.write(sequence_content)
                    safe_print(f"Saved sequence content to: {sequence_full_text_path}")

        except requests.RequestException as e:
            safe_print(f"Error processing {main_url}: {e}")
            continue

def process_csv_file(csv_file_path):
    safe_print(f"Processing CSV file: {csv_file_path}")
    data = fetch_urls_from_csv(csv_file_path)
    process_webpage(data, model_folder)

def main():
    # 获取list文件夹中的所有CSV文件
    csv_folder = './data/list'
    csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')]

    # 使用ThreadPoolExecutor并行处理CSV文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_csv_file, csv_file_path) for csv_file_path in csv_files]
        concurrent.futures.wait(futures)

    safe_print("All URLs and subpages fetched and processed successfully.")

if __name__ == "__main__":
    main()
