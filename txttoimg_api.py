from io import BytesIO
import base64

from flask import Flask, jsonify

from create_picture import create_picture

app = Flask(__name__)

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

@app.route("/txt2img", methods=["POST"])
def create_image():
    data = request.get_json()
    receipt_content = data.get("receipt_content")

    messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot who makes judgements about people based on their purchases. You can look at a receipt and guess a person's sex, age range, style of dress, hairstyle, level of body modification, etc.",
    },
    {"role": "user", "content": f"Please describe the profile of a person with the following purchses: {receipt_content}"},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    prompt = outputs[0]["generated_text"]


    img = create_picture(prompt)

    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_b64 = base64.b64encode(im_file.getvalue())

    return jsonify({"value": im_b64})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
