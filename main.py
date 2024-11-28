import json
import os
import platform

import pytesseract
import requests
import yaml
from PIL import Image

# Read Config File
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


if platform.system() == "Windows":
    # Path to Tesseract
    pytesseract.pytesseract.tesseract_cmd = config["win_tesseract_path"]
else:
    pass


# Read the text from the receipt image
FULL_IMAGE_PATH = os.path.join(os.getcwd(), config["image_filename"])
image = Image.open(FULL_IMAGE_PATH)
extracted_text = pytesseract.image_to_string(image)
print("Receipt contents:", extracted_text)

if platform.system() == "Windows":
    from create_picture import create_picture

    img = create_picture(response)
    img.save("output.png")
else:
    import base64

    response = requests.post("http://127.0.0.1:5000/txt2img", json={"receipt_content": extracted_text})
    print(response.json())
