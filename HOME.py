import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="LAPTOPS Project",
    page_icon="💻",
    layout="centered",  # or "wide" for full-width
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown(
    """
    <style>
        .big-title {
            font-size: 3em;
            font-weight: bold;
            color: #4F8BF9;
        }
        .subtitle {
            font-size: 1.2em;
            color: #666;
        }
        .footer {
            margin-top: 50px;
            font-size: 0.8em;
            color: #AAA;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MAIN TITLE ---
st.markdown('<div class="big-title">👋 Welcome to the LAPTOPS Project</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Made by <strong>Antra Das</strong></div>', unsafe_allow_html=True)

# --- DESCRIPTION / INTRO ---
st.write("""
This app is built to explore and analyze laptop specifications and pricing.  
Feel free to navigate through the sections using the sidebar on the left.

### ✨ What You’ll Find Inside:
- 💡 Laptop Price Predictor
- 📊 Data Visualizations
- 🔍 Laptop Specs Explorer
- 🧠 Machine Learning Insights
""")

# --- SIDEBAR INFO ---
st.sidebar.success("👈 Select a page from the sidebar")

# --- OPTIONAL FOOTER ---
st.markdown('<div class="footer">© 2025 Antra Das | Built with Streamlit</div>', unsafe_allow_html=True)
