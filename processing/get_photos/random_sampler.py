import os
import random
import shutil

def random_sample_files(photos_dir, annotations_dir, output_photos_dir, output_annotations_dir, sample_size):
    # Get list of files in photos directory
    photo_files = [f for f in os.listdir(photos_dir) if os.path.isfile(os.path.join(photos_dir, f))]
    
    # Extract base filenames (without extensions) for photos
    photo_base_names = [os.path.splitext(f)[0] for f in photo_files]
    
    # Randomly sample base names
    sampled_base_names = random.sample(photo_base_names, sample_size)
    
    # Create output directories if they don't exist
    os.makedirs(output_photos_dir, exist_ok=True)
    os.makedirs(output_annotations_dir, exist_ok=True)
    
    for base_name in sampled_base_names:
        # Copy the photo file
        photo_file = base_name + ".jpg"  # Assuming photo files are .jpg, change as needed
        photo_src = os.path.join(photos_dir, photo_file)
        photo_dst = os.path.join(output_photos_dir, photo_file)
        if os.path.exists(photo_src):
            shutil.copy(photo_src, photo_dst)
        
        # Copy the corresponding annotation file
        annotation_file = base_name + ".xml"  
        annotation_src = os.path.join(annotations_dir, annotation_file)
        annotation_dst = os.path.join(output_annotations_dir, annotation_file)
        if os.path.exists(annotation_src):
            shutil.copy(annotation_src, annotation_dst)

# Example usage
photos_dir = "/Volumes/My Passport for Mac/ty_saguaro_project/testing_data/resized_photos/set_1"
annotations_dir = "/Volumes/My Passport for Mac/ty_saguaro_project/data_all/set_1_labels/old_all_annotations_raw/Annotations"
output_photos_dir = "/Volumes/My Passport for Mac/ty_saguaro_project/testing_data/random_sample/photos"
output_annotations_dir = "/Volumes/My Passport for Mac/ty_saguaro_project/testing_data/random_sample/annotations"
sample_size = 50  # Adjust the sample size as needed

random_sample_files(photos_dir, annotations_dir, output_photos_dir, output_annotations_dir, sample_size)
