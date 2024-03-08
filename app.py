from flask import Flask, render_template, request, Response, make_response
from image_processor import process_image
from video_processor import process_video
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/img', methods=["GET", "POST"])
def predict_img():
    if request.method == 'POST':
        uploaded_file = request.files['fileInput']
        if uploaded_file.filename != '':
            # if uploaded file is a video
            if allowed_file(uploaded_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                # Get the original filename and format extension
                original_filename, extension = os.path.splitext(uploaded_file.filename)
                # Construct the new filename
                video_path = f'static/input{extension}'
                # video_path = 'static/video.mp4'
                uploaded_file.save(video_path)

                # Process the video file here
                vid_path, output = process_video(video_path)
                # print(output, vid_path, video_path)

                # Set Cache-Control header to no-cache to prevent caching of the image
                response = Response(render_template('index.html', results=vid_path))
                response.headers['Cache-Control'] = 'no-cache'
                return response
                # return 'Video uploaded successfully'

            # if uploaded file is an image
            elif allowed_file(uploaded_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                image_path = 'static/results.jpg'
                uploaded_file.save(image_path)
                image_results, output = process_image(image_path)
                print('Image uploaded successfully')

                # Set Cache-Control header to no-cache to prevent caching of the image
                response = Response(render_template('index.html', results=image_results))
                response.headers['Cache-Control'] = 'no-cache'
                return response
            # return render_template('index.html', results=image_results)
        else:
            return render_template('index.html', results='No file uploaded')
    return 'Error in uploading file'


if __name__ == '__main__':
    app.run(debug=True)
