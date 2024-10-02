import os
import json
from sklearn.model_selection import train_test_split

def load_and_combine_json(directory):
    combined_data = []
    # Walk through directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    # Open and read the JSON file
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        # Attempt to load JSON data, handling non-standard formats
                        data = json.load(json_file)
                        if isinstance(data, list):
                            # Extend if the data is a list of objects
                            combined_data.extend(data)
                        else:
                            # If not a list, append as a single object
                            combined_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error reading file {file_path}: {e}")
    return combined_data

def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main(input_dirs, output_dir, test_size=0.1):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load and combine JSON data from all input directories
    all_data = []
    for directory in input_dirs:
        all_data.extend(load_and_combine_json(directory))

    # Split the data into training and evaluation sets based on test_size ratio
    train_data, eval_data = train_test_split(all_data, test_size=test_size, random_state=42)

    # Save the training and evaluation datasets to JSON files in the output directory
    save_json(train_data, os.path.join(output_dir, 'train.json'))
    save_json(eval_data, os.path.join(output_dir, 'eval.json'))

    print("JSON files have been merged and split successfully.")

if __name__ == "__main__":
    # Directory containing the JSON files
    input_dirs = ['../Dataset']  # Modified to list, supporting multiple directories

    # Output directory where train.json and eval.json will be saved
    output_dir = '../Output'

    # Adjust the ratio for train and eval split (e.g., 1:10 for 10% eval data)
    test_size_ratio = 0.1

    main(input_dirs, output_dir, test_size=test_size_ratio)
