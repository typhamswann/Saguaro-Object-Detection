def filter_filenames(input_path, allowed_numbers):
    # Read the lines from the input file
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    # Filter the lines
    filtered_lines = [line for line in lines if int(line.split('_')[0]) in allowed_numbers]

    # Write the filtered lines back to the input file
    with open(input_path, 'w') as outfile:
        outfile.writelines(filtered_lines)

    print(f"Filtered filenames have been written back to {input_path}")

# List of allowed numbers
allowed_numbers = {1, 10, 11, 12, 13, 14, 16, 22, 27, 29, 31, 32, 36}

# Path to the input file
input_path = '/Volumes/My Passport for Mac/ty_saguaro_project/labels/old_all_annotations_raw/ImageSets/Segmentation/default.txt'

# Call the function
filter_filenames(input_path, allowed_numbers)
