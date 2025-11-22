import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pages.SQL import DB
from pages.PDHELPER import PY
from pathlib import Path

# Check if statsmodels is available for trendlines
try:
    import statsmodels
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

st.set_page_config(
    page_title="Premium Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5em;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1em;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to safely create plots
def safe_plot(plot_func, *args, **kwargs):
    """Safely create a plot with error handling"""
    try:
        return plot_func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error creating plot: {e}")
        return None

# Initialize data sources
@st.cache_data
def load_laptop_data():
    """Load all laptop data from database"""
    try:
        db = DB()
        if not db.conn or not db.cursor:
            return pd.DataFrame()
        query = """
            SELECT 
                Company, TypeName, Inches, ScreenSizeCategory,
                resolution_width, resolution_height, touchscreen, IPS_Panel, Full_HD,
                cpu_brand, cpu_speed, Ram, Memory_Type, Primary_Memory, Secondary_Memory,
                Gpu_brand, OpSys, Weight, Price
            FROM laptops
            WHERE Price IS NOT NULL AND Price > 0
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        columns = [desc[0] for desc in db.cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        
        # Convert Price to numeric, handling any string values
        if 'Price' in df.columns:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            df = df[df['Price'].notna() & (df['Price'] > 0)]
        
        # Convert other numeric columns
        numeric_cols = ['Inches', 'Ram', 'Primary_Memory', 'Secondary_Memory', 
                       'cpu_speed', 'Weight', 'resolution_width', 'resolution_height']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        db.conn.close()
        return df
    except Exception as e:
        print(f"Error loading laptop data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_smartphone_data():
    """Load smartphone data from CSV"""
    try:
        # Get the root directory (parent of pages)
        root_dir = Path(__file__).parent.parent
        csv_path = root_dir / "dataset" / "smartphone_cleaned_v2.csv"
        if not csv_path.exists():
            print(f"CSV file not found at: {csv_path}")
            return pd.DataFrame()
        df = pd.read_csv(csv_path)
        # Convert price to numeric and filter
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df = df[df['price'].notna() & (df['price'] > 0)]
        
        # Convert other numeric columns that might be strings
        numeric_cols = ['rating', 'screen_size', 'ram_capacity', 'internal_memory',
                       'battery_capacity', 'processor_speed', 'primary_camera_rear', 
                       'primary_camera_front', 'refresh_rate']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        print(f"Error loading smartphone data: {e}")
        return pd.DataFrame()

# Load data with error handling
try:
    laptop_df = load_laptop_data()
except Exception as e:
    st.error(f"Failed to load laptop data: {e}")
    laptop_df = pd.DataFrame()

try:
    smartphone_df = load_smartphone_data()
except Exception as e:
    st.error(f"Failed to load smartphone data: {e}")
    smartphone_df = pd.DataFrame()

# Main title
st.markdown('<div class="main-header">📊 Premium Data Analysis Dashboard</div>', unsafe_allow_html=True)

# Sidebar for category selection
st.sidebar.title("📈 Analysis Category")
category = st.sidebar.radio(
    "Select Category",
    ["💻 Laptops", "📱 Smartphones"],
    index=0
)

if category == "💻 Laptops":
    if laptop_df.empty:
        st.warning("⚠️ No laptop data available. Please check database connection.")
    elif 'Price' not in laptop_df.columns or 'Company' not in laptop_df.columns:
        st.error("⚠️ Required columns missing from laptop data. Please check database schema.")
        st.write("Available columns:", list(laptop_df.columns))
    else:
        st.header("💻 Laptop Analysis Dashboard")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Laptops", f"{len(laptop_df):,}")
        with col2:
            try:
                avg_price = float(laptop_df['Price'].mean())
                st.metric("Average Price", f"₹{avg_price:,.0f}")
            except (ValueError, TypeError) as e:
                st.metric("Average Price", "N/A")
        with col3:
            st.metric("Brands", f"{laptop_df['Company'].nunique()}")
        with col4:
            try:
                min_price = float(laptop_df['Price'].min())
                max_price = float(laptop_df['Price'].max())
                st.metric("Price Range", f"₹{min_price:,.0f} - ₹{max_price:,.0f}")
            except (ValueError, TypeError) as e:
                st.metric("Price Range", "N/A")
        
        st.divider()
        
        # Tab layout for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💰 Price Analysis", 
            "🏢 Brand Analysis", 
            "⚙️ Specifications", 
            "📈 Trends & Correlations",
            "🎯 Feature Impact"
        ])
        
        with tab1:
            st.subheader("💰 Price Distribution & Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Price Distribution Histogram
                fig_hist = px.histogram(
                    laptop_df, 
                    x='Price',
                    nbins=50,
                    title="Price Distribution",
                    labels={'Price': 'Price (₹)', 'count': 'Number of Laptops'},
                    color_discrete_sequence=['#667eea']
                )
                fig_hist.update_layout(
                    template='plotly_white',
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Price by Company (Box Plot)
                top_companies = laptop_df['Company'].value_counts().head(10).index
                df_top = laptop_df[laptop_df['Company'].isin(top_companies)]
                
                fig_box = px.box(
                    df_top,
                    x='Company',
                    y='Price',
                    title="Price Distribution by Top Brands",
                    labels={'Price': 'Price (₹)', 'Company': 'Brand'},
                    color='Company',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_box.update_layout(
                    template='plotly_white',
                    height=400,
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Price vs Specifications
            col1, col2 = st.columns(2)
            
            with col1:
                # Price vs RAM
                # Create a copy and fill NaN values in size column
                df_plot = laptop_df.copy()
                if 'Primary_Memory' in df_plot.columns:
                    # Ensure it's numeric
                    df_plot['Primary_Memory'] = pd.to_numeric(df_plot['Primary_Memory'], errors='coerce')
                    # Fill NaN with median or default
                    median_val = df_plot['Primary_Memory'].median() if df_plot['Primary_Memory'].notna().any() else 256
                    df_plot['Primary_Memory'] = df_plot['Primary_Memory'].fillna(median_val)
                    # Filter out rows where size column is still NaN or invalid
                    df_plot = df_plot[df_plot['Primary_Memory'].notna() & (df_plot['Primary_Memory'] > 0)]
                
                if not df_plot.empty and 'Primary_Memory' in df_plot.columns:
                    fig_ram = px.scatter(
                        df_plot,
                        x='Ram',
                        y='Price',
                        color='Company',
                        size='Primary_Memory',
                        hover_data=['TypeName', 'cpu_brand'],
                        title="Price vs RAM (colored by Brand)",
                        labels={'Ram': 'RAM (MB)', 'Price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_ram.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_ram, use_container_width=True)
                else:
                    # Fallback without size parameter
                    fig_ram = px.scatter(
                        laptop_df,
                        x='Ram',
                        y='Price',
                        color='Company',
                        hover_data=['TypeName', 'cpu_brand'],
                        title="Price vs RAM (colored by Brand)",
                        labels={'Ram': 'RAM (MB)', 'Price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_ram.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_ram, use_container_width=True)
            
            with col2:
                # Price vs Screen Size
                # Create a copy and fill NaN values in size column
                df_plot2 = laptop_df.copy()
                if 'Primary_Memory' in df_plot2.columns:
                    # Ensure it's numeric
                    df_plot2['Primary_Memory'] = pd.to_numeric(df_plot2['Primary_Memory'], errors='coerce')
                    # Fill NaN with median or default
                    median_val = df_plot2['Primary_Memory'].median() if df_plot2['Primary_Memory'].notna().any() else 256
                    df_plot2['Primary_Memory'] = df_plot2['Primary_Memory'].fillna(median_val)
                    df_plot2 = df_plot2[df_plot2['Primary_Memory'].notna() & (df_plot2['Primary_Memory'] > 0)]
                
                if not df_plot2.empty and 'Primary_Memory' in df_plot2.columns:
                    fig_screen = px.scatter(
                        df_plot2,
                        x='Inches',
                        y='Price',
                        color='ScreenSizeCategory',
                        size='Primary_Memory',
                        hover_data=['Company', 'TypeName'],
                        title="Price vs Screen Size",
                        labels={'Inches': 'Screen Size (inches)', 'Price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_screen.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_screen, use_container_width=True)
                else:
                    # Fallback without size parameter
                    fig_screen = px.scatter(
                        laptop_df,
                        x='Inches',
                        y='Price',
                        color='ScreenSizeCategory',
                        hover_data=['Company', 'TypeName'],
                        title="Price vs Screen Size",
                        labels={'Inches': 'Screen Size (inches)', 'Price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_screen.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_screen, use_container_width=True)
        
        with tab2:
            st.subheader("🏢 Brand Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Brand Count
                brand_counts = laptop_df['Company'].value_counts().head(15)
                fig_brand = px.bar(
                    x=brand_counts.values,
                    y=brand_counts.index,
                    orientation='h',
                    title="Number of Models by Brand",
                    labels={'x': 'Number of Models', 'y': 'Brand'},
                    color=brand_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_brand.update_layout(template='plotly_white', height=500, showlegend=False)
                st.plotly_chart(fig_brand, use_container_width=True)
            
            with col2:
                # Average Price by Brand
                avg_price_brand = laptop_df.groupby('Company')['Price'].mean().sort_values(ascending=False).head(15)
                fig_avg = px.bar(
                    x=avg_price_brand.index,
                    y=avg_price_brand.values,
                    title="Average Price by Brand",
                    labels={'x': 'Brand', 'y': 'Average Price (₹)'},
                    color=avg_price_brand.values,
                    color_continuous_scale='Plasma'
                )
                fig_avg.update_layout(template='plotly_white', height=500, xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig_avg, use_container_width=True)
            
            # Brand Market Share (Pie Chart)
            brand_counts_all = laptop_df['Company'].value_counts()
            fig_pie = px.pie(
                values=brand_counts_all.values,
                names=brand_counts_all.index,
                title="Brand Market Share",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab3:
            st.subheader("⚙️ Specifications Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CPU Brand Distribution
                cpu_dist = laptop_df['cpu_brand'].value_counts()
                fig_cpu = px.pie(
                    values=cpu_dist.values,
                    names=cpu_dist.index,
                    title="CPU Brand Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_cpu.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_cpu, use_container_width=True)
            
            with col2:
                # GPU Brand Distribution
                gpu_dist = laptop_df['Gpu_brand'].value_counts()
                fig_gpu = px.pie(
                    values=gpu_dist.values,
                    names=gpu_dist.index,
                    title="GPU Brand Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_gpu.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_gpu, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Memory Type Distribution
                mem_dist = laptop_df['Memory_Type'].value_counts()
                fig_mem = px.bar(
                    x=mem_dist.index,
                    y=mem_dist.values,
                    title="Memory Type Distribution",
                    labels={'x': 'Memory Type', 'y': 'Count'},
                    color=mem_dist.values,
                    color_continuous_scale='Blues'
                )
                fig_mem.update_layout(template='plotly_white', height=400, showlegend=False)
                st.plotly_chart(fig_mem, use_container_width=True)
            
            with col2:
                # Operating System Distribution
                os_dist = laptop_df['OpSys'].value_counts()
                fig_os = px.bar(
                    x=os_dist.index,
                    y=os_dist.values,
                    title="Operating System Distribution",
                    labels={'x': 'Operating System', 'y': 'Count'},
                    color=os_dist.values,
                    color_continuous_scale='Greens'
                )
                fig_os.update_layout(template='plotly_white', height=400, xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig_os, use_container_width=True)
            
            # RAM Distribution
            ram_counts = laptop_df['Ram'].value_counts().sort_index().head(10)
            fig_ram_dist = px.bar(
                x=ram_counts.index.astype(str),
                y=ram_counts.values,
                title="RAM Capacity Distribution",
                labels={'x': 'RAM (MB)', 'y': 'Number of Laptops'},
                color=ram_counts.values,
                color_continuous_scale='Purples'
            )
            fig_ram_dist.update_layout(template='plotly_white', height=400, showlegend=False)
            st.plotly_chart(fig_ram_dist, use_container_width=True)
        
        with tab4:
            st.subheader("📈 Trends & Correlations")
            
            # Correlation Heatmap
            numeric_cols = ['Price', 'Inches', 'Ram', 'Primary_Memory', 'Secondary_Memory', 
                           'cpu_speed', 'Weight', 'resolution_width', 'resolution_height']
            corr_df = laptop_df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_df,
                text_auto=True,
                aspect="auto",
                title="Feature Correlation Heatmap",
                color_continuous_scale='RdBu',
                labels=dict(color="Correlation")
            )
            fig_corr.update_layout(template='plotly_white', height=600)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Price vs CPU Speed
                scatter_kwargs = {
                    'x': 'cpu_speed',
                    'y': 'Price',
                    'color': 'cpu_brand',
                    'title': "Price vs CPU Speed",
                    'labels': {'cpu_speed': 'CPU Speed (GHz)', 'Price': 'Price (₹)'},
                    'color_discrete_sequence': px.colors.qualitative.Set3
                }
                if HAS_STATSMODELS:
                    scatter_kwargs['trendline'] = "ols"
                fig_cpu_speed = px.scatter(laptop_df, **scatter_kwargs)
                fig_cpu_speed.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_cpu_speed, use_container_width=True)
            
            with col2:
                # Price vs Weight
                scatter_kwargs = {
                    'x': 'Weight',
                    'y': 'Price',
                    'color': 'TypeName',
                    'title': "Price vs Weight",
                    'labels': {'Weight': 'Weight (kg)', 'Price': 'Price (₹)'},
                    'color_discrete_sequence': px.colors.qualitative.Pastel
                }
                if HAS_STATSMODELS:
                    scatter_kwargs['trendline'] = "ols"
                fig_weight = px.scatter(laptop_df, **scatter_kwargs)
                fig_weight.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_weight, use_container_width=True)
        
        with tab5:
            st.subheader("🎯 Feature Impact on Price")
            
            # Feature importance visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Average price by Type
                type_price = laptop_df.groupby('TypeName')['Price'].mean().sort_values(ascending=False)
                fig_type = px.bar(
                    x=type_price.index,
                    y=type_price.values,
                    title="Average Price by Laptop Type",
                    labels={'x': 'Laptop Type', 'y': 'Average Price (₹)'},
                    color=type_price.values,
                    color_continuous_scale='Viridis'
                )
                fig_type.update_layout(template='plotly_white', height=400, showlegend=False)
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                # Price by Screen Size Category
                screen_price = laptop_df.groupby('ScreenSizeCategory')['Price'].mean().sort_values(ascending=False)
                fig_screen_cat = px.bar(
                    x=screen_price.index,
                    y=screen_price.values,
                    title="Average Price by Screen Size Category",
                    labels={'x': 'Screen Size Category', 'y': 'Average Price (₹)'},
                    color=screen_price.values,
                    color_continuous_scale='Plasma'
                )
                fig_screen_cat.update_layout(template='plotly_white', height=400, showlegend=False)
                st.plotly_chart(fig_screen_cat, use_container_width=True)
            
            # Feature comparison: Touchscreen, IPS Panel, Full HD
            feature_cols = ['touchscreen', 'IPS_Panel', 'Full_HD']
            feature_data = []
            for feature in feature_cols:
                if feature in laptop_df.columns:
                    avg_price_yes = laptop_df[laptop_df[feature] == 1]['Price'].mean()
                    avg_price_no = laptop_df[laptop_df[feature] == 0]['Price'].mean()
                    feature_data.append({
                        'Feature': feature.replace('_', ' '),
                        'With Feature': avg_price_yes,
                        'Without Feature': avg_price_no
                    })
            
            if feature_data:
                feature_df = pd.DataFrame(feature_data)
                fig_feature = go.Figure()
                fig_feature.add_trace(go.Bar(
                    name='With Feature',
                    x=feature_df['Feature'],
                    y=feature_df['With Feature'],
                    marker_color='#667eea'
                ))
                fig_feature.add_trace(go.Bar(
                    name='Without Feature',
                    x=feature_df['Feature'],
                    y=feature_df['Without Feature'],
                    marker_color='#764ba2'
                ))
                fig_feature.update_layout(
                    title="Price Impact: Premium Features",
                    xaxis_title="Feature",
                    yaxis_title="Average Price (₹)",
                    template='plotly_white',
                    height=400,
                    barmode='group'
                )
                st.plotly_chart(fig_feature, use_container_width=True)

elif category == "📱 Smartphones":
    if smartphone_df.empty:
        st.warning("⚠️ No smartphone data available. Please check dataset file.")
    elif 'price' not in smartphone_df.columns or 'brand_name' not in smartphone_df.columns:
        st.error("⚠️ Required columns missing from smartphone data. Please check dataset file.")
        st.write("Available columns:", list(smartphone_df.columns))
    else:
        st.header("📱 Smartphone Analysis Dashboard")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Smartphones", f"{len(smartphone_df):,}")
        with col2:
            try:
                avg_price = float(smartphone_df['price'].mean())
                st.metric("Average Price", f"₹{avg_price:,.0f}")
            except (ValueError, TypeError) as e:
                st.metric("Average Price", "N/A")
        with col3:
            st.metric("Brands", f"{smartphone_df['brand_name'].nunique()}")
        with col4:
            try:
                min_price = float(smartphone_df['price'].min())
                max_price = float(smartphone_df['price'].max())
                st.metric("Price Range", f"₹{min_price:,.0f} - ₹{max_price:,.0f}")
            except (ValueError, TypeError) as e:
                st.metric("Price Range", "N/A")
        
        st.divider()
        
        # Tab layout for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💰 Price Analysis", 
            "🏢 Brand Analysis", 
            "📱 Specifications", 
            "📈 Trends & Correlations",
            "🎯 Feature Impact"
        ])
        
        with tab1:
            st.subheader("💰 Price Distribution & Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Price Distribution Histogram
                fig_hist = px.histogram(
                    smartphone_df, 
                    x='price',
                    nbins=50,
                    title="Price Distribution",
                    labels={'price': 'Price (₹)', 'count': 'Number of Smartphones'},
                    color_discrete_sequence=['#667eea']
                )
                fig_hist.update_layout(template='plotly_white', height=400, showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Price by Brand (Box Plot)
                top_brands = smartphone_df['brand_name'].value_counts().head(10).index
                df_top = smartphone_df[smartphone_df['brand_name'].isin(top_brands)]
                
                fig_box = px.box(
                    df_top,
                    x='brand_name',
                    y='price',
                    title="Price Distribution by Top Brands",
                    labels={'price': 'Price (₹)', 'brand_name': 'Brand'},
                    color='brand_name',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_box.update_layout(template='plotly_white', height=400, xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Price vs Specifications
            col1, col2 = st.columns(2)
            
            with col1:
                # Price vs RAM
                # Create a copy and fill NaN values in size column
                df_plot = smartphone_df.copy()
                if 'internal_memory' in df_plot.columns:
                    df_plot['internal_memory'] = pd.to_numeric(df_plot['internal_memory'], errors='coerce')
                    df_plot['internal_memory'] = df_plot['internal_memory'].fillna(df_plot['internal_memory'].median() if df_plot['internal_memory'].notna().any() else 128)
                    df_plot = df_plot[df_plot['internal_memory'].notna() & (df_plot['internal_memory'] > 0)]
                
                if not df_plot.empty and 'internal_memory' in df_plot.columns:
                    fig_ram = px.scatter(
                        df_plot,
                        x='ram_capacity',
                        y='price',
                        color='brand_name',
                        size='internal_memory',
                        hover_data=['model', 'processor_brand'],
                        title="Price vs RAM (colored by Brand)",
                        labels={'ram_capacity': 'RAM (GB)', 'price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_ram.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_ram, use_container_width=True)
                else:
                    # Fallback without size parameter
                    fig_ram = px.scatter(
                        smartphone_df,
                        x='ram_capacity',
                        y='price',
                        color='brand_name',
                        hover_data=['model', 'processor_brand'],
                        title="Price vs RAM (colored by Brand)",
                        labels={'ram_capacity': 'RAM (GB)', 'price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_ram.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_ram, use_container_width=True)
            
            with col2:
                # Price vs Screen Size
                # Create a copy and fill NaN values in size column
                df_plot2 = smartphone_df.copy()
                if 'battery_capacity' in df_plot2.columns:
                    df_plot2['battery_capacity'] = pd.to_numeric(df_plot2['battery_capacity'], errors='coerce')
                    df_plot2['battery_capacity'] = df_plot2['battery_capacity'].fillna(df_plot2['battery_capacity'].median() if df_plot2['battery_capacity'].notna().any() else 4000)
                    df_plot2 = df_plot2[df_plot2['battery_capacity'].notna() & (df_plot2['battery_capacity'] > 0)]
                
                if not df_plot2.empty and 'battery_capacity' in df_plot2.columns:
                    fig_screen = px.scatter(
                        df_plot2,
                        x='screen_size',
                        y='price',
                        color='brand_name',
                        size='battery_capacity',
                        hover_data=['model', 'resolution'],
                        title="Price vs Screen Size",
                        labels={'screen_size': 'Screen Size (inches)', 'price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_screen.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_screen, use_container_width=True)
                else:
                    # Fallback without size parameter
                    fig_screen = px.scatter(
                        smartphone_df,
                        x='screen_size',
                        y='price',
                        color='brand_name',
                        hover_data=['model', 'resolution'],
                        title="Price vs Screen Size",
                        labels={'screen_size': 'Screen Size (inches)', 'price': 'Price (₹)'},
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_screen.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_screen, use_container_width=True)
        
        with tab2:
            st.subheader("🏢 Brand Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Brand Count
                brand_counts = smartphone_df['brand_name'].value_counts().head(15)
                fig_brand = px.bar(
                    x=brand_counts.values,
                    y=brand_counts.index,
                    orientation='h',
                    title="Number of Models by Brand",
                    labels={'x': 'Number of Models', 'y': 'Brand'},
                    color=brand_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_brand.update_layout(template='plotly_white', height=500, showlegend=False)
                st.plotly_chart(fig_brand, use_container_width=True)
            
            with col2:
                # Average Price by Brand
                avg_price_brand = smartphone_df.groupby('brand_name')['price'].mean().sort_values(ascending=False).head(15)
                fig_avg = px.bar(
                    x=avg_price_brand.index,
                    y=avg_price_brand.values,
                    title="Average Price by Brand",
                    labels={'x': 'Brand', 'y': 'Average Price (₹)'},
                    color=avg_price_brand.values,
                    color_continuous_scale='Plasma'
                )
                fig_avg.update_layout(template='plotly_white', height=500, xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig_avg, use_container_width=True)
            
            # Brand Market Share (Pie Chart)
            brand_counts_all = smartphone_df['brand_name'].value_counts()
            fig_pie = px.pie(
                values=brand_counts_all.values,
                names=brand_counts_all.index,
                title="Brand Market Share",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab3:
            st.subheader("📱 Specifications Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Processor Brand Distribution
                proc_dist = smartphone_df['processor_brand'].value_counts()
                fig_proc = px.pie(
                    values=proc_dist.values,
                    names=proc_dist.index,
                    title="Processor Brand Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_proc.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_proc, use_container_width=True)
            
            with col2:
                # Operating System Distribution
                os_dist = smartphone_df['os'].value_counts()
                fig_os = px.pie(
                    values=os_dist.values,
                    names=os_dist.index,
                    title="Operating System Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_os.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig_os, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 5G Support Distribution
                if 'has_5g' in smartphone_df.columns:
                    g5_dist = smartphone_df['has_5g'].value_counts()
                    fig_5g = px.bar(
                        x=['No 5G', '5G Support'],
                        y=[g5_dist.get(False, 0), g5_dist.get(True, 0)],
                        title="5G Support Distribution",
                        labels={'x': '5G Support', 'y': 'Count'},
                        color=[g5_dist.get(False, 0), g5_dist.get(True, 0)],
                        color_continuous_scale='Blues'
                    )
                    fig_5g.update_layout(template='plotly_white', height=400, showlegend=False)
                    st.plotly_chart(fig_5g, use_container_width=True)
            
            with col2:
                # Fast Charging Distribution
                if 'fast_charging' in smartphone_df.columns:
                    fc_dist = smartphone_df['fast_charging'].value_counts()
                    fig_fc = px.bar(
                        x=fc_dist.index.astype(str) + 'W',
                        y=fc_dist.values,
                        title="Fast Charging Distribution",
                        labels={'x': 'Charging Speed', 'y': 'Count'},
                        color=fc_dist.values,
                        color_continuous_scale='Greens'
                    )
                    fig_fc.update_layout(template='plotly_white', height=400, showlegend=False)
                    st.plotly_chart(fig_fc, use_container_width=True)
            
            # RAM Distribution
            if 'ram_capacity' in smartphone_df.columns:
                ram_counts = smartphone_df['ram_capacity'].value_counts().sort_index().head(10)
                fig_ram_dist = px.bar(
                    x=ram_counts.index.astype(str) + ' GB',
                    y=ram_counts.values,
                    title="RAM Capacity Distribution",
                    labels={'x': 'RAM', 'y': 'Number of Smartphones'},
                    color=ram_counts.values,
                    color_continuous_scale='Purples'
                )
                fig_ram_dist.update_layout(template='plotly_white', height=400, showlegend=False)
                st.plotly_chart(fig_ram_dist, use_container_width=True)
        
        with tab4:
            st.subheader("📈 Trends & Correlations")
            
            # Correlation Heatmap
            numeric_cols = ['price', 'rating', 'screen_size', 'ram_capacity', 'internal_memory',
                           'battery_capacity', 'processor_speed', 'primary_camera_rear', 
                           'primary_camera_front']
            numeric_cols = [col for col in numeric_cols if col in smartphone_df.columns]
            
            if len(numeric_cols) > 1:
                corr_df = smartphone_df[numeric_cols].corr()
                
                fig_corr = px.imshow(
                    corr_df,
                    text_auto=True,
                    aspect="auto",
                    title="Feature Correlation Heatmap",
                    color_continuous_scale='RdBu',
                    labels=dict(color="Correlation")
                )
                fig_corr.update_layout(template='plotly_white', height=600)
                st.plotly_chart(fig_corr, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Price vs Rating
                if 'rating' in smartphone_df.columns:
                    scatter_kwargs = {
                        'x': 'rating',
                        'y': 'price',
                        'color': 'brand_name',
                        'title': "Price vs Rating",
                        'labels': {'rating': 'Rating', 'price': 'Price (₹)'},
                        'color_discrete_sequence': px.colors.qualitative.Set3
                    }
                    if HAS_STATSMODELS:
                        scatter_kwargs['trendline'] = "ols"
                    fig_rating = px.scatter(smartphone_df, **scatter_kwargs)
                    fig_rating.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_rating, use_container_width=True)
            
            with col2:
                # Price vs Battery Capacity
                if 'battery_capacity' in smartphone_df.columns:
                    scatter_kwargs = {
                        'x': 'battery_capacity',
                        'y': 'price',
                        'color': 'brand_name',
                        'title': "Price vs Battery Capacity",
                        'labels': {'battery_capacity': 'Battery (mAh)', 'price': 'Price (₹)'},
                        'color_discrete_sequence': px.colors.qualitative.Pastel
                    }
                    if HAS_STATSMODELS:
                        scatter_kwargs['trendline'] = "ols"
                    fig_battery = px.scatter(smartphone_df, **scatter_kwargs)
                    fig_battery.update_layout(template='plotly_white', height=400)
                    st.plotly_chart(fig_battery, use_container_width=True)
        
        with tab5:
            st.subheader("🎯 Feature Impact on Price")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Average price by OS
                if 'os' in smartphone_df.columns:
                    os_price = smartphone_df.groupby('os')['price'].mean().sort_values(ascending=False)
                    fig_os_price = px.bar(
                        x=os_price.index,
                        y=os_price.values,
                        title="Average Price by Operating System",
                        labels={'x': 'Operating System', 'y': 'Average Price (₹)'},
                        color=os_price.values,
                        color_continuous_scale='Viridis'
                    )
                    fig_os_price.update_layout(template='plotly_white', height=400, showlegend=False)
                    st.plotly_chart(fig_os_price, use_container_width=True)
            
            with col2:
                # Price by Processor Brand
                if 'processor_brand' in smartphone_df.columns:
                    proc_price = smartphone_df.groupby('processor_brand')['price'].mean().sort_values(ascending=False).head(10)
                    fig_proc_price = px.bar(
                        x=proc_price.index,
                        y=proc_price.values,
                        title="Average Price by Processor Brand",
                        labels={'x': 'Processor Brand', 'y': 'Average Price (₹)'},
                        color=proc_price.values,
                        color_continuous_scale='Plasma'
                    )
                    fig_proc_price.update_layout(template='plotly_white', height=400, xaxis_tickangle=-45, showlegend=False)
                    st.plotly_chart(fig_proc_price, use_container_width=True)
            
            # Feature comparison: 5G, NFC, Fast Charging
            feature_data = []
            if 'has_5g' in smartphone_df.columns:
                avg_price_5g = smartphone_df[smartphone_df['has_5g'] == True]['price'].mean()
                avg_price_no_5g = smartphone_df[smartphone_df['has_5g'] == False]['price'].mean()
                feature_data.append({
                    'Feature': '5G Support',
                    'With Feature': avg_price_5g,
                    'Without Feature': avg_price_no_5g
                })
            
            if 'has_nfc' in smartphone_df.columns:
                avg_price_nfc = smartphone_df[smartphone_df['has_nfc'] == True]['price'].mean()
                avg_price_no_nfc = smartphone_df[smartphone_df['has_nfc'] == False]['price'].mean()
                feature_data.append({
                    'Feature': 'NFC Support',
                    'With Feature': avg_price_nfc,
                    'Without Feature': avg_price_no_nfc
                })
            
            if feature_data:
                feature_df = pd.DataFrame(feature_data)
                fig_feature = go.Figure()
                fig_feature.add_trace(go.Bar(
                    name='With Feature',
                    x=feature_df['Feature'],
                    y=feature_df['With Feature'],
                    marker_color='#667eea'
                ))
                fig_feature.add_trace(go.Bar(
                    name='Without Feature',
                    x=feature_df['Feature'],
                    y=feature_df['Without Feature'],
                    marker_color='#764ba2'
                ))
                fig_feature.update_layout(
                    title="Price Impact: Premium Features",
                    xaxis_title="Feature",
                    yaxis_title="Average Price (₹)",
                    template='plotly_white',
                    height=400,
                    barmode='group'
                )
                st.plotly_chart(fig_feature, use_container_width=True)
