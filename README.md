# Video Audio Annotation ID Processing Scripts
This repository contains scripts that performs the following tasks:
1. Addition of ID to each cell in the video files
2. Link the Pho references of the video cells based on onset offset times
3. Addition of ID to %pho, %xcom, and annotations of the format [a-zA-Z]\_[a-zA-Z]\_[a-zA-Z]{3}
4. Addition of ID references between pho and chi, as well as detecting audio annotation file errors along the way
5. Check whether Annotation IDs are added to all words that are annotated. 

## Instruction
All those scripts require setting the input/output file path inside of the script before running. To run the audio processing scripts, pyclan is required
