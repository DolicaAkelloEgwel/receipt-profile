import base64
import json

import pytesseract
import requests
import torch
import yaml
from diffusers import StableDiffusionPipeline
from PIL import Image

# Read Config File
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]

# Stable Diffusion Setup
MODEL_ID = "OFA-Sys/small-stable-diffusion-v0"
pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Read the text from the receipt image
image = Image.open(config["input_image"])
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

# Create a picture
image = pipe(response + " 4K").images[0]
image.save("output.png")
