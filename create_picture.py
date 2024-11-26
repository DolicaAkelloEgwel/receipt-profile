import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = "OFA-Sys/small-stable-diffusion-v0"
pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
pipe = pipe.to("cuda")


# Create a picture
def create_picture(prompt: str):
    return pipe(prompt + " 4K").images[0]
