import imageio

def print_image_metadata(image_path):
    # Read the image
    image = imageio.imread(image_path)

    print(f"Filename: {image_path}")
    print(f"Image Shape: {image.shape}")
    print(f"Data Type: {image.dtype}")

# Replace 'path_to_your_image.jpg' with the path to your image file
image_path = '/Users/typham-swann/Downloads/36_2017_2017_06_22_07_1.jpg'
print_image_metadata(image_path)

