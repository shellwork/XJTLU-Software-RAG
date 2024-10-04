# -*- coding: utf-8 -*-

import pandas as pd
import os
import math
import concurrent.futures
import logging

# Configure logging to output to both console and a log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("split_csv_files.log"),
        logging.StreamHandler()
    ]
)

# Input and Output directories
INPUT_FOLDER = '../Input/'    # Path to the folder containing original CSV files
OUTPUT_FOLDER = './'  # Path to the folder where split CSV files will be saved

# Number of rows per split file
ROWS_PER_FILE = 20

def split_csv_by_rows(file_path, output_folder, rows_per_file=20):
    """
    Splits a CSV file into multiple smaller CSV files, each containing a specified number of rows.

    Parameters:
    - file_path (str): Path to the original CSV file.
    - output_folder (str): Directory where the split CSV files will be saved.
    - rows_per_file (int): Number of rows each split file should contain.

    Returns:
    - None
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        total_rows = len(df)
        logging.info(f"Processing file: {file_path} with {total_rows} rows.")

        # Calculate the number of split files needed
        num_parts = math.ceil(total_rows / rows_per_file)
        logging.info(f"Splitting into {num_parts} parts of up to {rows_per_file} rows each.")

        # Extract the base filename without extension for naming split files
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        for i in range(num_parts):
            # Determine the start and end indices for the current split
            start_idx = i * rows_per_file
            end_idx = start_idx + rows_per_file
            part_df = df.iloc[start_idx:end_idx]

            # Construct the output file path
            output_file = os.path.join(
                output_folder,
                f"{base_filename}_part_{i + 1}.csv"
            )

            # Save the split DataFrame to a new CSV file
            part_df.to_csv(output_file, index=False)
            logging.info(f"Saved split file: {output_file} with {len(part_df)} rows.")

    except Exception as e:
        logging.error(f"Failed to process file {file_path}. Error: {e}")

def get_all_csv_files(input_folder):
    """
    Retrieves all CSV file paths from the specified input directory.

    Parameters:
    - input_folder (str): Path to the input directory.

    Returns:
    - List[str]: A list of full paths to CSV files.
    """
    try:
        # List comprehension to get all CSV files in the input folder
        csv_files = [
            os.path.join(input_folder, file)
            for file in os.listdir(input_folder)
            if file.lower().endswith('.csv')
        ]
        logging.info(f"Found {len(csv_files)} CSV files in {input_folder}.")
        return csv_files
    except Exception as e:
        logging.error(f"Error accessing input folder {input_folder}. Error: {e}")
        return []

def create_output_folder(output_folder):
    """
    Creates the output directory if it does not exist.

    Parameters:
    - output_folder (str): Path to the output directory.

    Returns:
    - None
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        logging.info(f"Output folder is set to: {output_folder}")
    except Exception as e:
        logging.error(f"Failed to create output folder {output_folder}. Error: {e}")

def main():
    """
    Main function to orchestrate the splitting of CSV files.
    """
    # Create the output folder if it doesn't exist
    create_output_folder(OUTPUT_FOLDER)

    # Retrieve all CSV files from the input folder
    csv_files = get_all_csv_files(INPUT_FOLDER)

    if not csv_files:
        logging.warning("No CSV files found to process.")
        return

    # Optional: Use ThreadPoolExecutor for parallel processing of multiple CSV files
    # Adjust max_workers based on your system's capabilities
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit split tasks to the executor
        futures = [
            executor.submit(split_csv_by_rows, file, OUTPUT_FOLDER, ROWS_PER_FILE)
            for file in csv_files
        ]

        # Wait for all submitted tasks to complete
        concurrent.futures.wait(futures)

    logging.info("All CSV files have been successfully split.")

if __name__ == "__main__":
    main()
