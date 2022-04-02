from flask import Flask
from flask import jsonify, request
from text_extraction import download_image, read_text_from_image
import filetype
import os
import logging

app = Flask(__name__)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
logging.basicConfig()


@app.route('/text_recognition/<path:image_url>')
def text_recognition(image_url):
    image_path = download_image(image_url)
    if image_path and filetype.is_image(image_path):
        free_text = read_text_from_image(image_path)
        LOGGER.info(f"URL LINK : {image_url}")
        LOGGER.info(f"EXTRACTED TEXT : {free_text}")
        print("-" * 120)
        os.remove(image_path)
        return jsonify(data={'extracted_text': free_text})
    else:
        os.remove(image_path)
        return jsonify(data={'extracted_text': f'{image_url} not found or it is not an image file'}), 500


if __name__ == '__main__':
    app.run(port=8080)
