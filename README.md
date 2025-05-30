# merge-json
Made for merging spotify json data

## How to Use / Demo Video

https://www.youtube.com/watch?v=Bb_47VRS5Lg

<p align="left">
  <a href="https://www.youtube.com/watch?v=Bb_47VRS5Lg" title="Merge Json Video">
    <img src="https://img.youtube.com/vi/Bb_47VRS5Lg/hqdefault.jpg" alt="Merge Json Video" />
  </a>
</p>

## How to Use (description)

1.  **Clone the Repository (or download the files) and Add Files to Merge**
    *    Add json files you wish to combine (they must all be in the same directory as merge_json.py)
    *    Note: feel free to ignore any of the files in `jacoblam121's files`, that was just me using the script

3.  **Edit `files_to_merge.txt`:**
    *    Open `files_to_merge.txt` with a text editor. List the exact filenames of your Spotify JSON data files that you want to merge, with each filename on a new line.
    *   Ensure the filenames match exactly, including the `.json` extension.
    *   These files must also be present in the same directory as the script.
    *   You can add comments by starting a line with `#`. Empty lines are ignored.

    Example `files_to_merge.txt`:
    ```txt
    # List of Spotify JSON files to merge
    Streaming_History_Audio_2017-2022_0.json
    Streaming_History_Audio_2022_1.json
    Streaming_History_Audio_2022-2023_2.json
    Streaming_History_Audio_2023_3.json
    Streaming_History_Audio_2023_4.json
    Streaming_History_Audio_2023-2024_5.json
    Streaming_History_Audio_2024-2025_6.json
    Streaming_History_Audio_2025_7.json
    ```
4.  **Open a Terminal / CMD**
    CD into directory where files are

    For example:
    ```bash
    cd path/to/your_project_directory
    ```
    (Replace `path/to/your_project_directory` with the actual path.)

5.  **Run the Script:**
    Make sure you have python installed
    
     ```bash
    python merge_json.py
    ```
