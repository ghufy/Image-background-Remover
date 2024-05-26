from flask import Flask, render_template, request, send_file
from leapcell import Leapcell
from PIL import Image
from io import BytesIO
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

api = Leapcell(api_key=os.environ.get("LEAPCELL_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove_background", methods=["POST"])
def remove_background():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        img = Image.open(file)
        # Call your background removal function here
        # Example: img_no_bg = remove_background(img)
        
        # For demonstration, let's just invert the colors
        img_no_bg = Image.eval(img, lambda x: 255 - x)
        
        img_byte_arr = BytesIO()
        img_no_bg.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return send_file(img_byte_arr, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)