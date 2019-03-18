# Video Audio Annotation ID Processing Scripts
This repository contains scripts that performs the following tasks:
1. Addition of ID to each cell in the video files
2. Link the Pho references of the video cells based on onset offset times
3. Addition of ID to %pho, %xcom, and annotations of the format [a-zA-Z]\_[a-zA-Z]\_[a-zA-Z]{3}
4. Addition of ID references between pho and chi, as well as detecting audio annotation file errors along the way

## Instruction
All those scripts require setting the input/output file path inside of the script before running. To run the audio processing scripts, pyclan is required


### retrieve_codes.py usage

$ python retrieve_codes.py ../scatter/path_files/cha_sparse_code_paths.txt ../scatter/video_sparse_code_paths.txt batch


### delete_space_before_code.py

Correct mistake made when using script from one_time_scripts/replace_used_id.py (additional space inserted)
