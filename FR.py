from werkzeug.utils import secure_filename, validate_arguments
import face_recognition
import os
from flask.globals import request
import base64
import requests.models
import json

from flask import Flask, redirect, jsonify
from flask_restful import Api, Resource
# from requests.models import Responsepip
import os
app = Flask(__name__)
api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
final = ""

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'docx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class isHuman(Resource):
    def post(self):
        data = json.loads(request.data)
        if 'file' not in data:
            return jsonify({
                "status": False,
                "fileuploade": False

            })
        file = base64.b64decode(data['file'])
        with open('filename.jpg', 'wb') as f:
            f.write(file)

        if file:
            try:
                known_image = face_recognition.load_image_file('filename.jpg')
                encoding_1 = face_recognition.face_encodings(known_image)[0]
                return jsonify({
                    "image": "human"
                })
            except Exception:
                return({
                       "image": "please upload pic of human"
                       })
            finally:
                os.remove('filename.jpg')
        else:
            return({
                "Error": "Cannot be decoded"
            })


api.add_resource(isHuman, "/is_human")


class faceRecognition(Resource):
    def post(self):
        data = json.loads(request.data)
        if 'file' not in data:
            return jsonify({
                "status": False,
                "fileuploade": False

            })

        i = 0
        final = ""
        encoding_1 = 0
        encoding_2 = 0
        filesEncoded = data['file']
        filesDecoded = [base64.b64decode(f) for f in filesEncoded]
        j = 0
        for file in filesDecoded:
            with open('file'+str(j)+'.jpg', 'wb') as f:
                f.write(file)
                j += 1
        filesDecoded = os.listdir('./')
        for file in filesDecoded:
            if file.endswith('.jpg'):
                if i == 0:
                    known_image = face_recognition.load_image_file(file)
                    encoding_1 = face_recognition.face_encodings(known_image)[
                        0]
                    i = i+1
                else:
                    u_image = face_recognition.load_image_file(file)
                    encoding_2 = face_recognition.face_encodings(u_image)[0]
                    break
        final = ""
        results = face_recognition.compare_faces([encoding_1], encoding_2)
        if results[0]:
            final = "matched"
        else:
            final = "Not matched"
        for f in filesDecoded:
            if f.endswith('.jpg'):
                os.remove('./'+f)
        return jsonify({
            "output": final
        })


api.add_resource(faceRecognition, "/is_sameperson")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
