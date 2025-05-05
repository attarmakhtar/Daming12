from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("random_forest_model.pkl")

def analyze_prediction(pred):
    if isinstance(pred, str):
        return "Hasil tidak valid untuk dianalisis."
    if pred < 17:
        return "Termasuk dalam kategori *beton non-struktural* (kurang dari 17 MPa), tidak direkomendasikan untuk struktur utama."
    elif 17 <= pred < 40:
        return "Termasuk dalam kategori *beton struktural biasa* (17–40 MPa), cocok untuk struktur ringan hingga sedang."
    elif 40 <= pred < 80:
        return "Termasuk dalam kategori *beton kuat tinggi* (40–80 MPa), cocok untuk bangunan bertingkat atau jembatan."
    else:
        return "Termasuk dalam kategori *beton ultra high strength* (> 80 MPa), digunakan untuk struktur khusus dengan beban besar."

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    analysis = None
    if request.method == "POST":
        try:
            features = [float(request.form[f]) for f in [
                "cement", "slag", "flyash", "water",
                "superplasticizer", "coarseagg", "fineagg", "age"
            ]]
            prediction = model.predict([features])[0]
            analysis = analyze_prediction(prediction)
        except:
            prediction = "Input tidak valid"
            analysis = analyze_prediction(prediction)
    return render_template("index.html", prediction=prediction, analysis=analysis)

if __name__ == "__main__":
    app.run(debug=True)
