import os
import csv
import xml.etree.ElementTree as ET
from collections import Counter
from inference_sdk import InferenceHTTPClient

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

# Function to predict classes using the model
def predict(img_path):
    def count_classes(data):
        classes = [prediction['class'] for prediction in data['predictions']]
        class_counts = dict(Counter(classes))
        return class_counts

    # Initialize the client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=""
    )

    # Infer on a local image
    result = CLIENT.infer(img_path, model_id="cactus-detection-ynlrz/1")
    return count_classes(result)

# Function to process all files and save results to CSV
def process_directory_and_save_to_csv(image_dir, xml_dir, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Ground Truth', 'Predicted'])

        # Iterate through the directory with images
        for img_filename in os.listdir(image_dir):
            if img_filename.endswith(".jpg"):
                xml_filename = img_filename.replace('.jpg', '.xml')
                img_path = os.path.join(image_dir, img_filename)
                xml_path = os.path.join(xml_dir, xml_filename)

                # Count classes in XML (ground truth)
                ground_truth_counts = count_xml_classes(xml_path)

                # Predict classes using the model
                predicted_counts = predict(img_path)

                # Write the results to CSV
                writer.writerow([img_filename, ground_truth_counts, predicted_counts])

# Specify the directories and output file
image_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/data_all/set_2_photos"
xml_directory = "/Volumes/My Passport for Mac/ty_saguaro_project/data_all/set_2_labels/new_labeled_all/Annotations"
output_csv = "/Volumes/My Passport for Mac/ty_saguaro_project/set_2_results.csv"

# Process the directory and save results to CSV
process_directory_and_save_to_csv(image_directory, xml_directory, output_csv)






# import base64
# import requests
# from PIL import Image
# import io

# # Path to your image
# image_path = ''

# with Image.open(image_path) as img:
#     img = img.resize((640,640))  # Adjust the size as needed
#     buffered = io.BytesIO()
#     img.save(buffered, format="JPEG")
#     encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")


# # API endpoint and key
# url = "https://detect.roboflow.com/cactus-detection-ynlrz/1?api_key=ZBgjudlq4xdy0V1pL3SX"

# # Read the image and encode it as base64
# with open(image_path, "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# # Prepare the headers
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
# }

# # Send the encoded image in a POST request
# response = requests.post(url, data=encoded_image, headers=headers)

# # Print the response from the API
# print(response.text)


# # visualize your prediction
# # model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# # infer on an image hosted elsewhere
# # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())