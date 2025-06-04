# merge_json.py
import json
import os
import zipfile # Added for ZIP file handling
import argparse # Added for command-line argument parsing

# CONFIG_FILE_NAME = "files_to_merge.txt" # Removed
OUTPUT_FILE_NAME = "spotify_data.json"
TARGET_SUBFOLDER_FRAGMENT = "Spotify Extended Streaming History" # Added
AUDIO_FILE_PREFIX = "Streaming_History_Audio_" # Added

def merge_spotify_data(zip_file_path): # Modified function signature
    """
    Reads a Spotify data ZIP file, extracts and merges audio streaming history
    JSON files, and writes the combined list to a new JSON file.
    """
    all_records = []
    # input_files = [] # Removed

    # 1. Read the configuration file to get the list of JSON files # Removed section
    # print(f"Reading configuration from '{CONFIG_FILE_NAME}'...") # Removed
    # if not os.path.exists(CONFIG_FILE_NAME): # Removed
    #     print(f"Error: Configuration file '{CONFIG_FILE_NAME}' not found.") # Removed
    #     print("Please create it and list the JSON files to merge, one per line.") # Removed
    #     return # Removed

    # try: # Removed
    #     with open(CONFIG_FILE_NAME, 'r', encoding='utf-8') as f: # Removed
    #         for line in f: # Removed
    #             filename = line.strip() # Removed
    #             # Ignore empty lines and lines starting with # (comments) # Removed
    #             if filename and not filename.startswith('#'): # Removed
    #                 input_files.append(filename) # Removed
    # except Exception as e: # Removed
    #     print(f"Error reading configuration file '{CONFIG_FILE_NAME}': {e}") # Removed
    #     return # Removed

    # if not input_files: # Removed
    #     print("No input files specified in the configuration file. Exiting.") # Removed
    #     return # Removed

    # print(f"Found {len(input_files)} files to merge: {', '.join(input_files)}") # Removed

    print(f"Processing ZIP file: '{zip_file_path}'...")
    if not os.path.exists(zip_file_path):
        print(f"Error: ZIP file '{zip_file_path}' not found.")
        return
    
    if not zipfile.is_zipfile(zip_file_path):
        print(f"Error: '{zip_file_path}' is not a valid ZIP file.")
        return

    audio_files_processed = 0
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as spotify_zip:
            # Get a list of all files and directories in the zip
            name_list = spotify_zip.namelist()
            
            relevant_files_to_process = []

            for member_path in name_list:
                # Normalize path separators for reliable matching
                normalized_member_path = member_path.replace("\\\\", "/")
                
                # Check if the file is within the target subfolder and is an audio history JSON file
                if TARGET_SUBFOLDER_FRAGMENT in normalized_member_path and \
                   os.path.basename(normalized_member_path).startswith(AUDIO_FILE_PREFIX) and \
                   normalized_member_path.endswith(".json"):
                    relevant_files_to_process.append(member_path)
            
            if not relevant_files_to_process:
                print(f"No audio streaming history JSON files found in '{TARGET_SUBFOLDER_FRAGMENT}' inside the ZIP.")
                print(f"Looked for files starting with '{AUDIO_FILE_PREFIX}' and ending with '.json'.")
                return

            print(f"Found {len(relevant_files_to_process)} audio history files to merge:")
            for file_path_in_zip in relevant_files_to_process:
                print(f"  - {file_path_in_zip}")


            # 2. Process each identified audio JSON file from the ZIP
            for file_path_in_zip in relevant_files_to_process:
                print(f"Processing '{file_path_in_zip}' from ZIP...")
                try:
                    # Read the file content from the zip
                    # spotify_zip.read() returns bytes, so decode to string
                    json_bytes = spotify_zip.read(file_path_in_zip)
                    json_string = json_bytes.decode('utf-8')
                    
                    # Parse the JSON string
                    data = json.loads(json_string) # Use json.loads for strings
                    
                    if isinstance(data, list):
                        all_records.extend(data)
                        audio_files_processed += 1
                        print(f"  Added {len(data)} records from '{file_path_in_zip}'.")
                    else:
                        print(f"  Warning: Content of '{file_path_in_zip}' is not a list. Skipping this file's content.")
                except json.JSONDecodeError:
                    print(f"  Error: Could not decode JSON from '{file_path_in_zip}'. It might be corrupted or not valid JSON. Skipping.")
                except Exception as e:
                    print(f"  An unexpected error occurred while processing '{file_path_in_zip}': {e}. Skipping.")
    
    except zipfile.BadZipFile:
        print(f"Error: Could not open or read '{zip_file_path}'. It might be corrupted or not a ZIP file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while handling the ZIP file: {e}")
        return

    if audio_files_processed == 0 and not all_records: # Check if any audio files were actually processed
        print("\nNo audio files were successfully processed from the ZIP. Output file will not be created.")
        return
        
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
    parser = argparse.ArgumentParser(description="Merge Spotify streaming history data from a ZIP file.")
    parser.add_argument("zip_file_path", help="Path to the Spotify data ZIP file (e.g., my_spotify_data.zip)")
    args = parser.parse_args()

    merge_spotify_data(args.zip_file_path)