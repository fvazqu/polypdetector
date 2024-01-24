from flask import Flask, render_template, request
from image_processor import process_image


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/img', methods=["GET", "POST"])
def predict_img():
    if request.method == 'POST':
        # Get the URL from the form
        # url = request.form['url']
        uploaded_file = request.files['fileInput']
        if uploaded_file.filename != '':
            image_path = 'static/results.jpg'
            uploaded_file.save(image_path)
            image_results, output = process_image(image_path)

            # Use output to determine if polyp is detected or not
            result = 'Result: Polyp Not-detected'

            print(image_results, result)
            return render_template('index.html', results=image_results, output=result)
        return 'Error in uploading file'


if __name__ == '__main__':
    app.run(debug=True)
