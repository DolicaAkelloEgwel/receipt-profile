import base64
from io import BytesIO

from flask import Flask, jsonify, request

from create_picture import create_picture

app = Flask(__name__)


@app.route("/txt2img", methods=["POST"])
def create_image():
    data = request.get_json()
    prompt = data.get("prompt")
    img = create_picture(prompt)

    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_b64 = base64.b64encode(im_file.getvalue())

    return jsonify({"value": im_b64})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
