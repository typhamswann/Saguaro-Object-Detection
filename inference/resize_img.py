from PIL import Image
import os

def resize_images(input_dir, output_dir, size=(800, 600)):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open an image file
            img = Image.open(os.path.join(input_dir, filename))
            # Resize image
            img_resized = img.resize(size)
            # Save resized image to the output directory
            img_resized.save(os.path.join(output_dir, filename))
            print(f'Resized and copied: {filename}')
        else:
            print(f'Skipped: {filename} (not an image file)')

# Example usage
input_directory = '/Volumes/My Passport for Mac/ty_saguaro_project/data_all/set_1_photos'
output_directory = '/Volumes/My Passport for Mac/ty_saguaro_project/resized_photos/set_1'
resize_images(input_directory, output_directory, size=(1707, 1280))
