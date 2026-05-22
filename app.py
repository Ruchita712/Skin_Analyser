from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from predict import predict_skin
from recommendations import recommendations
from report_generator import generate_report
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")
UPLOAD_FOLDER = "static/uploads"
REPORT_FOLDER = "static/reports"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        flash("No image file was submitted. Please choose a valid image.")
        return redirect(url_for('home'))

    file = request.files['image']
    if file.filename == '':
        flash("Please select an image before clicking Analyze.")
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        flash("Unsupported file type. Please upload a .png, .jpg, .jpeg or .gif image.")
        return redirect(url_for('home'))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    condition, confidence = predict_skin(path)
    recommendation = recommendations.get(condition, {
        "description": "No recommendation available.",
        "products": [],
        "routine": []
    })

    generate_report(condition, confidence, recommendation)

    image_url = url_for('static', filename=f'uploads/{filename}')
    return render_template(
        "results.html",
        condition=condition,
        confidence=confidence,
        recommendation=recommendation,
        image_url=image_url
    )


@app.route('/download')
def download():
    return send_file(
        os.path.join(REPORT_FOLDER, "report.pdf"),
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)