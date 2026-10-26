import joblib
import pandas as pd
from flask import Flask, jsonify, request

superkart_api = Flask("SuperKart Sales Predictor")

# Full preprocessing + model pipeline
model = joblib.load("superkart_model.joblib")

FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type", "Product_Id_char",
    "Store_Age_Years", "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


@superkart_api.post("/v1/predict")
def predict_sales():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Request body must be JSON"}), 400
    missing = [f for f in FEATURES if f not in payload]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    input_df = pd.DataFrame([{f: payload[f] for f in FEATURES}])
    prediction = float(model.predict(input_df)[0])
    return jsonify({"Predicted_Sales": round(prediction, 2)})


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    uploaded = request.files.get("file")
    if uploaded is None:
        return jsonify({"error": "Upload a CSV file under the 'file' field"}), 400

    input_df = pd.read_csv(uploaded)
    missing = [f for f in FEATURES if f not in input_df.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    predictions = model.predict(input_df[FEATURES])
    return jsonify({str(i): round(float(p), 2) for i, p in enumerate(predictions)})


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
