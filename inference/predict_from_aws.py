import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import roboflow

s3 = boto3.client(
    's3',
    region_name='us-east-1',  # Replace with your region code
    aws_access_key_id='',
    aws_secret_access_key=''
)

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket and return the S3 URL"""
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        # Upload the file to S3
        s3.upload_file(file_name, bucket, object_name)

        # Construct the S3 URL
        url = f"https://{bucket}.s3.amazonaws.com/{object_name}"
        return url
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return None
    except NoCredentialsError:
        print("Credentials not available.")
        return None
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return None

def run_inference_on_s3_images(folder_path, bucket, inference_function):
    """Upload images to S3 and run inference on them"""
    s3_urls = []

    # Upload each image to S3 and get the URL
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, file_name)
            url = upload_to_s3(file_path, bucket)
            if url:
                s3_urls.append(url)

    # Run the inference function on each S3 URL
    for url in s3_urls:
        inference_result = inference_function(url)
        print(f"Inference result for {url}: {inference_result}")

# Example usage
def my_inference_function(url):

    rf = roboflow.Roboflow(api_key="")

    project = rf.workspace().project("cactus-detection-ynlrz")
    model = project.version("1").model

    model.confidence = 50
    model.overlap = 25

    image_path = url

    prediction = model.predict(image_path, hosted=True)

    return prediction.json()

# Folder containing your images
folder_path = '/Volumes/My Passport for Mac/ty_saguaro_project/resized_photos/set_1'

# Name of your S3 bucket
bucket = 'saguaro-training-set-1'

# Run the script
run_inference_on_s3_images(folder_path, bucket, my_inference_function)

