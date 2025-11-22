import streamlit as st
from pages.SQL import DB  # Make sure dbhelper.py exists in the same folder
import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import joblib


st.set_page_config(page_title="LAPTOPS")

# Sidebar menu
st.sidebar.title("CATEGORY")
user_option = st.sidebar.selectbox("Select", ["Laptops_Analysis", "Laptop_Prediction"])

# Create DB instance
db = DB()

# Laptops section
if user_option == "Laptops_Analysis":
    st.title("💻 LAPTOPS")

    col1, col2 = st.columns(2)

    with col1:
        # Fetch and show companies in dropdown
        company_list = db.company_available()
        selected_company = st.selectbox("Select Company", company_list)
        
    with col2:
        # You can put more filters here (e.g., RAM, Processor)
        type_name = db.Typename()
        selected_type = st.selectbox("Select Type", type_name)


    if st.button("Search"):
        rows, cols = db.your_search(selected_company, selected_type)
        if rows:
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df)
        else:
            st.warning("No records found!")
    
if user_option == "Laptop_Prediction":
    st.title("💻 LAPTOP PRICE PREDICTION")

    # Assuming these functions exist and return lists or unique values
    company_list = db.company_available()
    selected_company = st.selectbox("Select Company", company_list)

    type_name_list = db.Typename()
    selected_type = st.selectbox("Select Type", type_name_list)

    inches_list = db.Inches()  # e.g., list of floats like [13.3, 14, 15.6, ...]
    selected_inches = st.selectbox("Select Inches", inches_list)

    screen_size_categories = db.ScreenSizeCategory()
    selected_screen_size_category = st.selectbox("Screen Size Category", screen_size_categories)

    resolution_width_list = db.resolution_width()  # e.g., [1366, 1920, 2560, ...]
    selected_resolution_width = st.selectbox("Resolution Width", resolution_width_list)

    resolution_height_list = db.resolution_height()  # e.g., [768, 1080, 1440, ...]
    selected_resolution_height = st.selectbox("Resolution Height", resolution_height_list)

    touchscreen = st.selectbox("Touchscreen", [0, 1])  # 0 = No, 1 = Yes

    ips_panel = st.selectbox("IPS Panel", [0, 1])  # 0 = No, 1 = Yes

    full_hd = st.selectbox("Full HD", [0, 1])  # 0 = No, 1 = Yes

    cpu_brands = db.cpu_brand()
    selected_cpu_brand = st.selectbox("CPU Brand", cpu_brands)

    cpu_speed_list = db.cpu_speed()  # e.g., [1.6, 2.4, 3.1, ...]
    selected_cpu_speed = st.selectbox("CPU Speed (GHz)", cpu_speed_list)

    ram_list = db.Ram() # e.g., [4, 8, 16, 32]
    selected_ram = st.selectbox("RAM (MB)", ram_list)

    memory_types = db.Memory_Type()
    selected_memory_type = st.selectbox("Memory Type", memory_types)

    primary_memory_list = db.Primary_Memory()  # e.g., [256, 512, 1024, ...]
    selected_primary_memory = st.selectbox("Primary Memory (GB)", primary_memory_list)

    secondary_memory_list = db.Secondary_Memory()  # e.g., [0, 256, 512, ...]
    selected_secondary_memory = st.selectbox("Secondary Memory (GB)", secondary_memory_list)

    gpu_brands = db.Gpu_brand()
    selected_gpu_brand = st.selectbox("GPU Brand", gpu_brands)

    opsys_list = db.OpSys()
    selected_opsys = st.selectbox("Operating System", opsys_list)

    weight_list = db.Weight() # e.g., [1.2, 1.5, 2.0, 2.5]
    selected_weight = st.selectbox("Weight (kg)", weight_list)

    # When user clicks predict:
    if st.button("Predict Price"):
        input_data = {
             'id' : 0,
            'Company': selected_company,
            'TypeName': selected_type,
            'Inches': selected_inches,
            'ScreenSizeCategory': selected_screen_size_category,
            'resolution_width': selected_resolution_width,
            'resolution_height': selected_resolution_height,
            'touchscreen': touchscreen,
            'IPS_Panel': ips_panel,
            'Full_HD': full_hd,
            'cpu_brand': selected_cpu_brand,
            'cpu_speed': selected_cpu_speed,
            'Ram': selected_ram,
            'Memory_Type': selected_memory_type,
            'Primary_Memory': selected_primary_memory,
            'Secondary_Memory': selected_secondary_memory,
            'Gpu_brand': selected_gpu_brand,
            'OpSys': selected_opsys,
            'Weight': selected_weight
        }

        input_df = pd.DataFrame([input_data])

        # Load pipeline using relative path for deployment compatibility
        pipeline_path = Path(__file__).parent.parent / 'pipeline' / 'xgb1_pipeline.pkl'
        pipeline = joblib.load(pipeline_path)

        predicted_price = pipeline.predict(input_df)[0]

        st.success(f"Estimated Laptop Price: ₹{predicted_price:,.2f}")


   
