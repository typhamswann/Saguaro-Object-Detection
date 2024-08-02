import boto3
import os
import csv
import xml.etree.ElementTree as ET
from collections import Counter
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import roboflow

# AWS S3 setup
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

def my_inference_function(url):
    rf = roboflow.Roboflow(api_key="")
    project = rf.workspace().project("cactus-detection-ynlrz")
    model = project.version("1").model

    prediction = model.predict(url, confidence=30, overlap=50, hosted=True)
    return prediction.json()

# Function to count classes in XML files (ground truth)
def count_xml_classes(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    class_names = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        class_names.append(class_name)

    class_counts = dict(Counter(class_names))
    return class_counts

def count_classes(data):
    classes = [prediction['class'] for prediction in data['predictions']]
    class_counts = dict(Counter(classes))
    return class_counts

# Main function to process the directory
def process_directory_and_save_to_csv(image_dir, xml_dir, bucket, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Ground Truth', 'Predicted'])

        # Iterate through the directory with images
        for img_filename in os.listdir(image_dir):
            if img_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                xml_filename = img_filename.replace('.jpg', '.xml')
                img_path = os.path.join(image_dir, img_filename)
                xml_path = os.path.join(xml_dir, xml_filename)

                # Upload image to S3 and get URL
                s3_url = upload_to_s3(img_path, bucket)

                if s3_url:
                    # Run inference on the image
                    inference_result = my_inference_function(s3_url)
                    predicted_counts = count_classes(inference_result)

                    # Count classes in XML (ground truth)
                    ground_truth_counts = count_xml_classes(xml_path)

                    # Write the results to CSV
                    writer.writerow([img_filename, ground_truth_counts, predicted_counts])

# Specify the directories and output file
image_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/testing_data/random_sample/photos"
xml_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/testing_data/random_sample/annotations"
bucket = 'saguaro-training-set-1'
output_csv = "/Volumes/My Passport for Mac/ty_saguaro_project/results/random_30c_50o_results.csv"

# TEST
# image_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/test_data/test_photos"
# xml_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/test_data/test_annotations"
# output_csv = "/Volumes/My Passport for Mac/ty_saguaro_project/test_results.csv"

# Process the directory and save results to CSV
process_directory_and_save_to_csv(image_directory, xml_directory, bucket, output_csv)
