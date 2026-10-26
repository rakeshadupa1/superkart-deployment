import os

import pandas as pd
import requests
import streamlit as st

# Backend container name on the shared Docker network
BACKEND_URL = os.getenv("BACKEND_URL", "http://superkart-backend:7860")

st.title("SuperKart Sales Forecast")
st.write("Predict the total sales of a product in a store.")

st.subheader("Online prediction")
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
id_char = st.selectbox("Product Id Prefix", ["FD", "NC", "DR"])
store_age = st.number_input("Store Age (years)", min_value=0, value=16)
type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

if st.button("Predict"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": sugar,
        "Product_Allocated_Area": area,
        "Product_MRP": mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": type_category,
    }
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
    if response.ok:
        st.success(f"Predicted sales: {response.json()['Predicted_Sales']:,.2f}")
    else:
        st.error(f"Prediction failed: {response.text}")

st.subheader("Batch prediction")
uploaded = st.file_uploader("Upload a CSV file", type="csv")
if uploaded is not None and st.button("Predict batch"):
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded.getvalue()}, timeout=60)
    if response.ok:
        df = pd.read_csv(uploaded)
        df["Predicted_Sales"] = list(response.json().values())
        st.dataframe(df)
    else:
        st.error(f"Batch prediction failed: {response.text}")
