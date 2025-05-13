from flask import Flask, request, jsonify
from src.database import db
import requests

class FaceVerify:
    

    def __init__(self):
        self.session = db.session()

    def verify_face(self, request):
        
        LAMBDA_URL = "https://7fsjznx53egw3utvtvtwpxbkxe0glbuh.lambda-url.us-east-2.on.aws/"
        if 'file' not in request.files or 'url' not in request.form:
            return jsonify({'error': 'Missing file or url'}), 400

        image_file = request.files['file']
        avatar_url = request.form['url']

        try:
            files = {
                'file': (image_file.filename, image_file.stream, image_file.content_type),
            }
            data = {
                'url': avatar_url
            }

            lambda_response = requests.post(LAMBDA_URL, files=files, data=data, timeout=60)

            if lambda_response.status_code != 200:
                return jsonify({'error': 'Lambda request failed', 'details': lambda_response.text}), 502

            return jsonify(lambda_response.json())

        except Exception as e:
            return jsonify({'error': str(e)}), 500