from ultralytics import YOLO
import os
from PIL import Image
import cv2

# Define the path to your custom YOLO model
local_model_path = 'polyp6.pt'

# Check if the model file exists locally
if os.path.isfile(local_model_path):
    # The model file exists, you can proceed with using it
    model = YOLO(local_model_path)

else:
    # The model file doesn't exist, you may want to handle this case
    print(f"Error: Model file '{local_model_path}' not found.")


def process_image(image_path):
    try:
        image = cv2.imread(image_path)

        # Run image on YOLO Model
        results = model.predict(image)

        # Save Image
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            image_path = 'static/results.jpg'
            im.save(image_path)  # save image

        # Output response
        output = "The image has been processed through the YOLO model"

        return image_path, output

    except Exception as e:
        # Handle any exceptions that occurred during image retrieval or processing
        error_message = str(e)
        return None, error_message  # Return None for the image and the error message
