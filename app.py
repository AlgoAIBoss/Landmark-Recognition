import io
import os
from google.cloud import vision
from flask import Flask, app, config , render_template , request
from flask_uploads import UploadSet , configure_uploads , IMAGES
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= r"ADD YOUR VISION API KEY.JSON HERE"
app = Flask(__name__)

photos = UploadSet('photos' , IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app , photos)

def detect_landmark(path):

    client = vision.ImageAnnotatorClient()

    with io.open(path , 'rb') as image_file:

        content = image_file.read()

    image = vision.Image(content = content)

    response = client.landmark_detection(image = image)

    #landmarks = response.landmark_annotations

    return response.landmark_annotations

@app.route('/' , methods=['GET' , 'POST'])
def upload() :

    if request.method == 'POST' and 'photo' in request.files :

        filename = photos.save(request.files['photo'])
        full_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)

        landmarks = detect_landmark(full_path)

        predictions = []

        for landmark in landmarks :

            predictions.append(landmark.description)

        prediction_text = ", ".join(predictions)

    else :

        prediction_text = "Nothing to predict..."


    return render_template('upload.html', prediction_text = prediction_text)

if __name__ == '__main__' :

    app.run(debug = True)
