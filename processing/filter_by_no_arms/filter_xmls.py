import os

def filter_xml_files(directory_path, allowed_numbers):
    # List all files in the directory
    files = os.listdir(directory_path)
    
    kept_files = []
    removed_files = []
    
    # Iterate over the files
    for filename in files:
        if filename.endswith('.xml'):
            # Extract the number from the start of the filename
            number = int(filename.split('_')[0])
            # If the number is in the allowed list, keep the file, otherwise remove it
            if number in allowed_numbers:
                kept_files.append(filename)
            else:
                os.remove(os.path.join(directory_path, filename))
                removed_files.append(filename)
    
    print("Kept files:")
    for file in kept_files:
        print(file)
    
    print("\nRemoved files:")
    for file in removed_files:
        print(file)

# List of allowed numbers
allowed_numbers = {1, 10, 11, 12, 13, 14, 16, 22, 27, 29, 31, 32, 36}

# Path to the directory containing XML files
directory_path = '/Volumes/My Passport for Mac/ty_saguaro_project/labels/old_all_annotations_raw/Annotations'

# Call the function
filter_xml_files(directory_path, allowed_numbers)
