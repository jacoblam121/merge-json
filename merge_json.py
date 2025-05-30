# merge_json.py
import json
import os

CONFIG_FILE_NAME = "files_to_merge.txt"
OUTPUT_FILE_NAME = "spotify_data.json"

def merge_spotify_data():
    """
    Reads a list of JSON filenames from a configuration file,
    merges their contents (assuming each is a list of objects),
    and writes the combined list to a new JSON file.
    """
    all_records = []
    input_files = []

    # 1. Read the configuration file to get the list of JSON files
    print(f"Reading configuration from '{CONFIG_FILE_NAME}'...")
    if not os.path.exists(CONFIG_FILE_NAME):
        print(f"Error: Configuration file '{CONFIG_FILE_NAME}' not found.")
        print("Please create it and list the JSON files to merge, one per line.")
        return

    try:
        with open(CONFIG_FILE_NAME, 'r', encoding='utf-8') as f:
            for line in f:
                filename = line.strip()
                # Ignore empty lines and lines starting with # (comments)
                if filename and not filename.startswith('#'):
                    input_files.append(filename)
    except Exception as e:
        print(f"Error reading configuration file '{CONFIG_FILE_NAME}': {e}")
        return

    if not input_files:
        print("No input files specified in the configuration file. Exiting.")
        return

    print(f"Found {len(input_files)} files to merge: {', '.join(input_files)}")

    # 2. Process each input JSON file
    for file_path in input_files:
        print(f"Processing '{file_path}'...")
        if not os.path.exists(file_path):
            print(f"  Warning: File '{file_path}' not found. Skipping.")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Each Spotify history file is a list of JSON objects
                data = json.load(f)
                if isinstance(data, list):
                    all_records.extend(data)
                    print(f"  Added {len(data)} records from '{file_path}'.")
                else:
                    print(f"  Warning: Content of '{file_path}' is not a list. Skipping this file's content.")
        except json.JSONDecodeError:
            print(f"  Error: Could not decode JSON from '{file_path}'. It might be corrupted or not valid JSON. Skipping.")
        except Exception as e:
            print(f"  An unexpected error occurred while processing '{file_path}': {e}. Skipping.")

    # 3. Write the combined data to the output file
    if not all_records:
        print("\nNo records were collected. Output file will not be created.")
        return

    print(f"\nTotal records collected: {len(all_records)}")
    print(f"Writing combined data to '{OUTPUT_FILE_NAME}'...")
    try:
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(all_records, f, indent=2) # indent=2 makes the output JSON human-readable
        print(f"Successfully merged data into '{OUTPUT_FILE_NAME}'.")
    except IOError as e:
        print(f"Error writing output file '{OUTPUT_FILE_NAME}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing output: {e}")

if __name__ == "__main__":
    merge_spotify_data()