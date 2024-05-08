from flask import Flask, render_template, request
import easyocr
import cv2
import os

app = Flask(__name__)

# Set up EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to perform OCR on the uploaded image
def perform_ocr(image_path):
    result = reader.readtext(image_path)
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            # Save the uploaded file to a temporary location
            file_path = 'uploads/' + file.filename
            file.save(file_path)

            # Perform OCR on the uploaded image
            result = perform_ocr(file_path)

            # Delete the uploaded file after OCR
            os.remove(file_path)

            # Render the template with the OCR result
            return render_template('index.html', result=result)

    # Render the initial template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
