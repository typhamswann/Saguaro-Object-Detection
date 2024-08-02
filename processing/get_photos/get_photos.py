import os
import shutil

def move_photos(parent_dir, txt_file, new_dir):
    # Read the text file and create a set of photo filenames
    with open(txt_file, 'r') as file:
        photo_filenames = set(line.strip() for line in file)
    
    photo_paths_count = len(photo_filenames)
    photos_found_count = 0

    # Create the new directory if it does not exist
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    # Walk through the parent directory
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                # Get the filename without extension
                filename_without_ext = os.path.splitext(file)[0]
                
                # Check if the filename is in the set
                if filename_without_ext in photo_filenames:
                    # Construct the full path of the photo
                    full_path = os.path.join(root, file)
                    
                    # Copy the photo to the new directory without preserving the directory structure
                    new_path = os.path.join(new_dir, file)
                    
                    shutil.copy2(full_path, new_path)
                    photos_found_count += 1
                    print(f"Copied: {full_path} to {new_path}")
    
    print(f"Total photos listed in text file: {photo_paths_count}")
    print(f"Total photos found and copied: {photos_found_count}")

# Example usage
parent_directory_path = '/Volumes/My Passport for Mac/ty_saguaro_project/saguaro_photos'
txt_file_path = '/Volumes/My Passport for Mac/ty_saguaro_project/labels/old_all_annotations_raw/ImageSets/Main/default.txt'
new_directory_path = '/Volumes/My Passport for Mac/ty_saguaro_project/set_1_photos'

move_photos(parent_directory_path, txt_file_path, new_directory_path)
