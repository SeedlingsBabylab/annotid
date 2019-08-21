# Video and Audio Annotation ID (annotid) Processing Scripts
This repository contains scripts that perform the following tasks:
1. Addition of ID to each cell in the video files
2. Link the Pho references of the video cells based on onset offset times
3. Addition of ID to %pho, %xcom, and annotations of the format [a-zA-Z]\_[a-zA-Z]\_[a-zA-Z]{3}
4. Addition of ID references between pho and chi, as well as detecting audio annotation file errors along the way
5. Check whether Annotation IDs are added to all words that are annotated. 

## Instruction
All those scripts require setting the input/output file path inside of the script before running. To run the audio processing scripts, pyclan is required


### retrieve_codes.py usage

$ python retrieve_codes.py ../scatter/path_files/cha_sparse_code_paths.txt ../scatter/video_sparse_code_paths.txt batch


### delete_space_before_code.py

Correct mistake made when using script from one_time_scripts/replace_used_id.py (additional space inserted)

### check_fixme.py

One time script -- retrieves files that have FIXME in wrong column, example of output in fixme_errors_audio.txt

### merge_bl_new_id

One time script to add annotid column to basic level

### move_no_id

One time script that moved files with no_id in name to folder named old_files
 
### undo_id

Removes all annotid from file
