import shutil
import glob

output_file_name = "input/combined_data.txt"

# Get all the files in the input directory
input_files = glob.glob("input/*.txt")

# Open the output file
with open(output_file_name, "wb") as output_file:
    # Iterate through the input files
    for input_file in input_files:
        if input_file == output_file_name:
            # Don't want to copy the output into the output
            continue

        else:
            with open(input_file, "rb") as file:
                shutil.copyfileobj(file, output_file)