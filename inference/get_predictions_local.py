import roboflow

# Initialize Roboflow with your API key
rf = roboflow.Roboflow(api_key="")

# Load the project and model version
project = rf.workspace().project("cactus-detection-ynlrz")
model = project.version("1").model

# Optionally, change the confidence and overlap thresholds
# Values are percentages
model.confidence = 50
model.overlap = 25

image_path = "https://res.cloudinary.com/do5ail0ju/image/upload/v1722573044/test_img_zm8kvm.jpg"

prediction = model.predict(image_path, hosted=True)

# Plot the prediction in an interactive environment (implementation needed)

# Convert predictions to JSON
print(prediction.json())
