import streamlit as st
import pandas as pd
import joblib
import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from PDHELPER import PY  # your helper class

# Load helper
py = PY()

st.title("💻 Smartphone Price Prediction")

# --- Collect inputs from user ---
brand = st.selectbox("Select Brand", py.brand_name())
model = st.selectbox("Select Model", py.model())
rating = st.slider("Rating", 
                   min_value=py.rating()["min"], 
                   max_value=py.rating()["max"], 
                   value=py.rating()["default"])

has_5g = st.selectbox("5G Support", py.has_5g())
has_nfc = st.selectbox("NFC Support", py.has_nfc())
has_ir = st.selectbox("IR Blaster", py.has_ir_blaster())

processor_name = st.selectbox("Processor Name", py.processor_name())
processor_brand = st.selectbox("Processor Brand", py.processor_brand())
num_cores = st.selectbox("CPU Cores", py.num_cores())

processor_speed = st.slider("Processor Speed (GHz)", 
                            min_value=py.processor_speed()["min"], 
                            max_value=py.processor_speed()["max"], 
                            value=py.processor_speed()["default"])

battery_capacity = st.slider("Battery Capacity (mAh)", 
                             min_value=py.battery_capacity()["min"], 
                             max_value=py.battery_capacity()["max"], 
                             value=py.battery_capacity()["default"])

fast_charging = st.selectbox("Fast Charging Support", py.fast_charging())

ram_capacity = st.slider("RAM (GB)", 
                         min_value=py.ram_capacity()["min"], 
                         max_value=py.ram_capacity()["max"], 
                         value=py.ram_capacity()["default"])

internal_memory = st.slider("Internal Storage (GB)", 
                            min_value=py.internal_memory()["min"], 
                            max_value=py.internal_memory()["max"], 
                            value=py.internal_memory()["default"])

screen_size = st.slider("Screen Size (inches)", 
                        min_value=py.screen_size()["min"], 
                        max_value=py.screen_size()["max"], 
                        value=py.screen_size()["default"])

refresh_rate = st.selectbox("Refresh Rate (Hz)", py.refresh_rate())
resolution = st.selectbox("Resolution", py.resolution())

num_rear_cameras = st.selectbox("Number of Rear Cameras", py.num_rear_cameras())
num_front_cameras = st.selectbox("Number of Front Cameras", py.num_front_cameras())

# --- Add missing inputs for required columns ---
primary_camera_front = st.slider("Primary Front Camera (MP)", 1, 40, 12)
primary_camera_rear = st.slider("Primary Rear Camera (MP)", 1, 108, 48)
os = st.selectbox("Operating System", ["Android", "iOS", "Other"])
extended_memory = st.selectbox("Extended Memory Support", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")

# --- Prediction button ---
if st.button("Predict Price"):
    # Prepare input as DataFrame
    input_data = pd.DataFrame([{
        "brand_name": brand,
        "model": model,
        "rating": rating,
        "has_5g": has_5g,
        "has_nfc": has_nfc,
        "has_ir_blaster": has_ir,
        "processor_name": processor_name,
        "processor_brand": processor_brand,
        "num_cores": num_cores,
        "processor_speed": processor_speed,
        "battery_capacity": battery_capacity,
        "fast_charging": fast_charging,
        "ram_capacity": ram_capacity,
        "internal_memory": internal_memory,
        "screen_size": screen_size,
        "refresh_rate": refresh_rate,
        "resolution": resolution,
        "num_rear_cameras": num_rear_cameras,
        "num_front_cameras": num_front_cameras,
        "primary_camera_front": primary_camera_front,
        "primary_camera_rear": primary_camera_rear,
        "os": os,
        "extended_memory": extended_memory
    }])

    # Load your trained pipeline
    model_path = Path("C:/laptops/pipeline/xgb_price_pipeline.pkl")
    pipeline = joblib.load(model_path)

    # Make prediction
    prediction = pipeline.predict(input_data)[0]
    st.success(f"📱 Predicted Price: ₹{prediction:,.2f}")
