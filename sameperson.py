from werkzeug.utils import secure_filename, validate_arguments
import face_recognition
import os
from flask.globals import request
import requests
import requests.models

from flask import Flask, redirect
from flask_restful import Api, Resource
# from requests.models import Responsepip
import os
app = Flask(__name__)
api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
final=""

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'docx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class getextension(Resource):
    def post(self):
        
        
        if 'file' not in request.files:
            return ({
                "status": False,
                "fileuploade": False

            })
         
        i=0
        final=""
        encoding_1=0;
        encoding_2=0;
        for file in request.files.getlist('file'):
            if file and allowed_file(file.filename):

                if i==0:
                    known_image = face_recognition.load_image_file(file)
                    encoding_1 = face_recognition.face_encodings(known_image)[0]
                    i=i+1
                else:
                     u_image = face_recognition.load_image_file(file)
                     encoding_2 = face_recognition.face_encodings(u_image)[0]
                     break
                     
                    

            else:
                return({
                        "allowedextensionsare": " png, jpg, jpeg"
                })
        final=""
        results = face_recognition.compare_faces([encoding_1], encoding_2)
        if results[0]:
            final="matched"
        else:
            final="Not matched"        
        return({
            "output":final
        })

        
api.add_resource(getextension, "/is_sameperson")

if __name__ == "__main__":
    app.run(debug=True)
