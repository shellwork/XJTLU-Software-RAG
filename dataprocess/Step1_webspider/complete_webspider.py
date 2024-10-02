# -*- coding: utf-8 -*-

import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
import csv
import time

# Global settings
csv_folder = '../Input'  # Path to the CSV folder
text_folder = '../Data'  # Folder for saving text

# Choose which parts to scrape, set to True to fetch
fetch_model = False  # Whether to fetch the model section
fetch_protocol = False  # Whether to fetch the protocol section
fetch_parts = False  # Whether to fetch the parts section
fetch_description = True  # Corrected spelling from fetch_decription to fetch_description
# Configuration options
download_texts = True

# Session settings
request_timeout = 60
max_retries = 3  # Set the maximum number of retries


def safe_filename(base_filename, suffix=''):
    """
    Generate a safe filename, ensuring it is ASCII compatible.
    """
    base_filename = re.sub(r'[^\w\s-]', '_', base_filename)  # Replace non-word characters with underscores
    ascii_filename = base_filename.encode('ascii', 'ignore').decode('ascii')  # Ensure ASCII compatibility
    return ascii_filename + suffix + '.txt'


def safe_print(content):
    """
    Safely print content, handling any encoding issues.
    """
    try:
        print(content.encode('utf-8', 'replace').decode('utf-8'))
    except UnicodeEncodeError:
        print("Error printing content due to encoding issues.")


def check_url(url):
    """
    Function to check if the URL returns a valid response.
    """
    try:
        response = requests.get(url, timeout=request_timeout)
        # Check for valid status code (200)
        return response.status_code == 200
    except requests.RequestException:
        # If the request fails for any reason, return False
        return False


def fetch_urls_from_csv(file_path):
    """
    Fetch URLs, year, and team name from a CSV file.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            year = row['year']
            team_name = row['team']
            base_url = row['wiki']

            data.append({
                'year': year,
                'team_name': team_name,
                'base_url': base_url
            })
    return data


def get_valid_subpage_urls(main_url, soup):
    """
    Get all valid subpage URLs that contain "parts.igem.org/Part:".
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
    Fetch the sequence page for a specific part number.
    """
    sequence_url = f"https://parts.igem.org/cgi/partsdb/composite_edit/putseq.cgi?part={parts_number}"
    session = requests.Session()
    for attempt in range(max_retries):
        try:
            sequence_response = session.get(sequence_url, timeout=request_timeout)
            if sequence_response.status_code == 404:
                safe_print(f"Sequence page not found: {sequence_url}")
                return None

            sequence_response.raise_for_status()
            return sequence_response.text
        except requests.RequestException as e:
            safe_print(f"Error fetching sequence page {sequence_url}: {e}")
            if attempt < max_retries - 1:
                safe_print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                return None


def discover_urls(year, team_name, base_url):
    """
    Discover and validate URLs to scrape starting from the base_root.
    If base_root is accessible, scrape the homepage and find relevant navigation links.

    Parameters:
    - year (str): The year of the team.
    - team_name (str): The name of the team.
    - base_url (str): The base URL from the CSV file.

    Returns:
    - dict: A dictionary of discovered URLs for different page types.
            Returns None if base_url is not accessible.
    """
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Check if base_url is accessible
    try:
        safe_print(f"Checking base URL for {team_name} ({year}): {base_url}")
        response = session.get(base_url, timeout=request_timeout, headers=headers)
        if response.status_code == 404:
            safe_print(f"Base URL not found (404): {base_url}. Skipping team {team_name} ({year}).")
            return None
        response.raise_for_status()
    except requests.RequestException as e:
        safe_print(f"Error accessing base URL {base_url}: {e}. Skipping team {team_name} ({year}).")
        return None

    # Parse the homepage
    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')

    # Initialize dictionary to hold discovered URLs
    discovered_urls = {}

    # Define desired page types
    desired_page_types = ['model', 'protocol', 'parts', 'index', 'description', 'design', 'engineering', 'contribution',
                          'experiments']

    # Find all navigation links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)

        # Check if the link belongs to the team's domain
        path = parsed_url.path
        if re.match(rf'^/Team:{re.escape(team_name)}/', path, re.IGNORECASE) or \
                re.match(rf'^/{re.escape(team_name)}/', path, re.IGNORECASE):
            # Extract the page type from the URL
            page_type = path.split('/')[-1].lower()
            if page_type in desired_page_types:
                discovered_urls[page_type] = full_url

    # Additionally, ensure that 'index' page is included
    if 'index' not in discovered_urls:
        discovered_urls['index'] = base_url  # Assuming base_url is the index

    safe_print(f"Discovered URLs for {team_name} ({year}): {discovered_urls}")
    return discovered_urls


def process_webpage(session, url, year, team_name, page_type, suffix='', text_folder=text_folder):
    """
    Process a single webpage and its subpages, downloading the text of each URL and its subpages.

    Parameters:
    - session (requests.Session): The session object for making HTTP requests.
    - url (str): The URL of the webpage to process.
    - year (str): The year associated with the team.
    - team_name (str): The name of the team.
    - page_type (str): The type of the page (e.g., 'protocol', 'parts').
    - suffix (str): Optional suffix for the filename.
    - text_folder (str): The base folder to save the text content.

    Returns:
    - bool: True if processing is successful, False otherwise.
    """
    for attempt in range(max_retries):
        try:
            safe_print(f"Processing {page_type} page for {team_name} ({year}): {url}")
            response = session.get(url, timeout=request_timeout)
            if response.status_code == 404:
                safe_print(f"Page not found (404): {url}")
                return False

            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')

            # Create a folder to save different page types
            folder_path = os.path.join(text_folder, page_type)
            os.makedirs(folder_path, exist_ok=True)

            # Process the main page
            filename = f"{year}_{team_name}_{page_type}"
            full_text_path = os.path.join(folder_path, safe_filename(filename, suffix))

            if download_texts:
                text_content = ' '.join(soup.stripped_strings)
                with open(full_text_path, 'w', encoding='utf-8', errors='replace') as file:
                    file.write(text_content)
                safe_print(f"Saved {page_type} page text to: {full_text_path}")

            # Process subpages (for the parts section)
            if page_type == 'parts':
                subpage_urls = get_valid_subpage_urls(url, soup)
                for sub_url in subpage_urls:
                    safe_print(f"Processing subpage: {sub_url}")
                    sub_response = session.get(sub_url, timeout=request_timeout)
                    if sub_response.status_code == 404:
                        safe_print(f"Subpage not found (404): {sub_url}")
                        continue

                    sub_response.raise_for_status()
                    sub_soup = BeautifulSoup(sub_response.content, 'lxml', from_encoding='utf-8')

                    parts_number = urlparse(sub_url).path.split(':')[-1]
                    sub_filename = f"{year}_{team_name}_{parts_number}"
                    sub_full_text_path = os.path.join(folder_path, safe_filename(sub_filename))

                    if download_texts:
                        sub_text_content = ' '.join(sub_soup.stripped_strings)
                        with open(sub_full_text_path, 'w', encoding='utf-8', errors='replace') as sub_file:
                            sub_file.write(sub_text_content)
                        safe_print(f"Saved subpage text to: {sub_full_text_path}")

                    # Fetch and save the sequence page
                    sequence_content = fetch_sequence_page(parts_number)
                    if sequence_content:
                        sequence_filename = f"{year}_{team_name}_{parts_number}_sequence"
                        sequence_full_text_path = os.path.join(folder_path, safe_filename(sequence_filename))
                        with open(sequence_full_text_path, 'w', encoding='utf-8', errors='replace') as sequence_file:
                            sequence_file.write(sequence_content)
                        safe_print(f"Saved sequence content to: {sequence_full_text_path}")

            return True  # Successfully processed
        except requests.RequestException as e:
            safe_print(f"Error processing {page_type} page {url}: {e}")
            if attempt < max_retries - 1:
                safe_print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                return False  # Failed after all retries


def process_csv_file(csv_file_path):
    """
    Process a single CSV file: discover URLs and process each webpage accordingly.

    Parameters:
    - csv_file_path (str): Path to the CSV file to process.

    Returns:
    - None
    """
    safe_print(f"Processing CSV file: {csv_file_path}")
    data = fetch_urls_from_csv(csv_file_path)
    for entry in data:
        year = entry['year']
        team_name = entry['team_name']
        base_url = entry['base_url']

        # Discover URLs starting from base_root
        discovered_urls = discover_urls(year, team_name, base_url)
        if not discovered_urls:
            continue  # Skip this entry if base_url is not accessible

        # Initialize a new session for each team to ensure thread safety
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Update discovered_urls to include only desired page types based on global settings
        urls_to_fetch = {}
        if fetch_model and 'model' in discovered_urls:
            urls_to_fetch['model'] = discovered_urls['model']
        if fetch_protocol and 'protocol' in discovered_urls:
            urls_to_fetch['protocol'] = discovered_urls['protocol']
        if fetch_parts and 'parts' in discovered_urls:
            urls_to_fetch['parts'] = discovered_urls['parts']
        if fetch_description:
            # Always fetch index and description regardless of other settings
            if 'index' in discovered_urls:
                urls_to_fetch['index'] = discovered_urls['index']
            if 'description' in discovered_urls:
                urls_to_fetch['description'] = discovered_urls['description']
            if 'design' in discovered_urls:
                urls_to_fetch['design'] = discovered_urls['design']
            if 'engineering' in discovered_urls:
                urls_to_fetch['engineering'] = discovered_urls['engineering']
            if 'contribution' in discovered_urls:
                urls_to_fetch['contribution'] = discovered_urls['contribution']

        # Process each URL based on the desired page types
        for page_type, url in urls_to_fetch.items():
            process_webpage(session, url, year, team_name, page_type)

        # Close the session after processing all URLs for the team
        session.close()


def main():
    """
    Main function to orchestrate the processing of all CSV files in parallel.
    """
    # Get all CSV files from the CSV folder
    csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')]

    # Use ThreadPoolExecutor to process CSV files in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_csv_file, csv_file_path) for csv_file_path in csv_files]
        concurrent.futures.wait(futures)

    safe_print("All URLs and subpages have been successfully fetched and processed.")


if __name__ == "__main__":
    main()
