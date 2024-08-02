import os

def remove_unlisted_files(txt_file_path, xml_directory):
    # Read the list of filenames from the txt file
    with open(txt_file_path, 'r') as txt_file:
        listed_files = set(line.strip() + '.xml' for line in txt_file)

    # List all files in the specified directory
    all_files = os.listdir(xml_directory)

    kept_files = []
    removed_files = []

    # Loop through all files in the directory
    for file in all_files:
        # Check if the file is an XML file
        if file.endswith('.xml'):
            # Check if the file is in the list
            if file in listed_files:
                kept_files.append(file)
            else:
                # Construct the full file path
                file_path = os.path.join(xml_directory, file)
                # Remove the file
                os.remove(file_path)
                removed_files.append(file_path)

    # Print the results
    print('Kept files:')
    for file in kept_files:
        print(file)

    print('\nRemoved files:')
    for file_path in removed_files:
        print(file_path)


# Example usage
txt_file_path = '/Volumes/My Passport for Mac/ty_saguaro_project/processing/default_removed.txt'
xml_directory = '/Volumes/My Passport for Mac/ty_saguaro_project/labels/old_all_annotations_raw/Annotations'
remove_unlisted_files(txt_file_path, xml_directory)
