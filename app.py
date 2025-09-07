from flask import Flask, request, jsonify
import joblib
import numpy as np
import sqlite3

model = joblib.load("house_price_model.pkl")

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            overall_qual INTEGER,
            gr_liv_area REAL,
            garage_cars INTEGER,
            total_bsmt_sf REAL,
            full_bath INTEGER,
            year_built INTEGER,
            predicted_price REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()  

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0]

    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO predictions (overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath, year_built, predicted_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (*data["features"], float(prediction)))
    conn.commit()
    conn.close()

    return jsonify({"predicted_price": float(prediction)})

@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    results = [
        {
            "id": r[0],
            "overall_qual": r[1],
            "gr_liv_area": r[2],
            "garage_cars": r[3],
            "total_bsmt_sf": r[4],
            "full_bath": r[5],
            "year_built": r[6],
            "predicted_price": r[7]
        }
        for r in rows
    ]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
