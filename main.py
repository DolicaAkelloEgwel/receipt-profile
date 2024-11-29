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
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


# Read the text from the receipt image
FULL_IMAGE_PATH = os.path.join(os.getcwd(), config["image_filename"])
image = Image.open(FULL_IMAGE_PATH)
extracted_text = pytesseract.image_to_string(image)
print("Receipt contents:", extracted_text)


def talk_to_ollama(url, data):

    response = requests.post(
        url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
    )

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
        return "Error: " + str(response.status_code) + response.text


# Get Ollama to analyse the customer
generate_profile_data = {
    "model": config["ollama_model"],
    "prompt": f"Here s the text from a receipt: {extracted_text}. Given what is on this receipt, can you please GUESS the sex, race, height, style of dress, age range, etc of the customer. You guess does not need to be accurate. You are simply making an assumption about the *type* of person who might buy such things.",
    "stream": False,
}

response = talk_to_ollama(config["ollama_url"], generate_profile_data)
if "Error" in response:
    print("Unable to generate customer description", response)
    exit()
print(response)

if platform.system() == "Windows":
    from create_picture import create_picture

    img = create_picture(response)
    img.save("output.png")
else:
    import base64

    response = requests.post("http://localhost:8000/txt2img", data=json.dumps({"prompt": response}))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["value"]
    else:
        print("Error: " + str(response.status_code) + response.text)
