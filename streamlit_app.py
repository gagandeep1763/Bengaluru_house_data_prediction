import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Bengaluru House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('Cleaned_data.csv')
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load model with compatibility handling
@st.cache_resource
def load_model():
    try:
        import pickle
        try:
            with open("RidgeModel.pki", 'rb') as f:
                model = pickle.load(f)
            return model
        except:
            st.warning("⚠️ Model loading failed. Using fallback prediction method.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Helper function to format prices in lakhs/crores
def format_price(price):
    """Format price in lakhs and crores"""
    try:
        if price >= 10000000:  # 1 crore
            return f"₹{price/10000000:.2f} Cr"
        elif price >= 100000:  # 1 lakh
            return f"₹{price/100000:.2f} L"
        else:
            return f"₹{price:,.0f}"
    except:
        return f"₹{price:,.0f}"

# Simple prediction function as fallback
def simple_predict(location, sqft, bath, bhk, data):
    try:
        location_data = data[data['location'] == location]
        
        if location_data.empty:
            avg_price = data['price'].mean()
        else:
            avg_price = location_data['price'].mean()
        
        price_per_sqft = avg_price / location_data['total_sqft'].mean() if not location_data.empty else data['price'].mean() / data['total_sqft'].mean()
        
        base_price = sqft * price_per_sqft
        
        bhk_factor = 1 + (bhk - 2) * 0.15
        bath_factor = 1 + (bath - 2) * 0.1
        
        final_price = base_price * bhk_factor * bath_factor
        
        return final_price
    except:
        return 5000000

# Load data and model
data = load_data()
model = load_model()

if data is None:
    st.error("❌ Could not load the dataset. Please check if 'Cleaned_data.csv' exists.")
    st.stop()

# Get unique locations
locations = sorted(data['location'].unique())

# Main title
st.markdown('<h1 class="main-header">🏠 Bengaluru House Price Predictor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Introduction
st.markdown("""
<div style="text-align: center; padding: 1rem; background: #f0f8ff; border-radius: 10px; margin-bottom: 2rem;">
    <h3 style="margin: 0; color: #0f172a; font-weight: 800;">Predict house prices in Bengaluru using advanced machine learning</h3>
    <p style="margin: 6px 0 0 0; color: #334155;">Get accurate price estimates based on location, property size, and amenities</p>
</div>
""", unsafe_allow_html=True)

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📋 Property Details")
    
    # Location selection
    location = st.selectbox(
        "📍 Select Location:",
        options=locations,
        index=0,
        help="Choose the area/location of the property"
    )
    
    # BHK input
    bhk = st.number_input(
        "🏠 Number of BHK:",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        help="Number of Bedrooms, Hall, and Kitchen"
    )

with col2:
    st.markdown("### 🏡 Property Features")
    
    # Bathrooms input
    bath = st.number_input(
        "🚿 Number of Bathrooms:",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        help="Number of bathrooms in the property"
    )
    
    # Square footage input
    sqft = st.number_input(
        "📏 Total Square Feet:",
        min_value=100,
        max_value=10000,
        value=1000,
        step=50,
        help="Total area of the property in square feet"
    )
    
    # Property type
    property_type = st.selectbox(
        "🏢 Property Type:",
        ["Apartment", "Independent House", "Villa", "Plot", "Other"],
        help="Type of property"
    )

with col3:
    st.markdown("### 📊 Quick Stats")
    
    if location:
        try:
            location_data = data[data['location'] == location]
            
            if not location_data.empty:
                avg_price = location_data['price'].mean()
                avg_sqft = location_data['total_sqft'].mean()
                count_properties = len(location_data)
                
                st.metric("🏘️ Properties in Area", f"{count_properties:,}")
                # Format average price in lakhs/crores
                if avg_price >= 10000000:
                    avg_price_display = f"₹{avg_price/10000000:.2f} Cr"
                elif avg_price >= 100000:
                    avg_price_display = f"₹{avg_price/100000:.2f} L"
                else:
                    avg_price_display = f"₹{avg_price:,.0f}"
                
                st.metric("💰 Avg Price", avg_price_display)
                st.metric("📐 Avg Size", f"{avg_sqft:.0f} sq ft")
            else:
                st.info("No data for this location")
        except:
            st.info("Loading stats...")

# Prediction button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🔮 Predict House Price", use_container_width=True):
        if location and bhk and bath and sqft:
            with st.spinner("Analyzing market data and calculating price..."):
                try:
                    if model is not None:
                        input_data = pd.DataFrame([[location, sqft, bath, bhk]], 
                                                columns=['location', 'total_sqft', 'bath', 'bhk'])
                        prediction = model.predict(input_data)[0] * 1e5
                    else:
                        prediction = simple_predict(location, sqft, bath, bhk, data)
                    
                    # Display result
                    st.markdown("---")
                    st.markdown("### 🎯 Prediction Result")
                    
                    # Format price in lakhs and crores
                    price_display = format_price(prediction)
                    
                    # Create a beautiful prediction display
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h2>Estimated Price</h2>
                        <h1 style="font-size: 3rem; margin: 1rem 0;">{price_display}</h1>
                        <p>Based on {location} • {bhk} BHK • {bath} Bath • {sqft} sq ft</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Price analysis removed per request
                    
                    # Additional insights
                    st.markdown("### 📊 **Market Intelligence**")
                    # Compute price per square foot for analysis
                    price_per_sqft = prediction / max(sqft, 1)
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🎯 **Investment Value**")
                        if price_per_sqft >= 12000:
                            st.success("**High ROI Potential**")
                            st.write("Premium location with strong appreciation prospects")
                        elif price_per_sqft >= 8000:
                            st.info("**Good Investment**")
                            st.write("Stable market with steady growth potential")
                        else:
                            st.warning("**Affordable Option**")
                            st.write("Entry-level pricing, good for first-time buyers")
                    
                    with col2:
                        st.markdown("#### 📈 **Market Position**")
                        if prediction >= 10000000:
                            st.success("**Luxury Segment**")
                            st.write("High-end property market")
                        elif prediction >= 5000000:
                            st.info("**Mid-Range Market**")
                            st.write("Popular segment with good demand")
                        else:
                            st.warning("**Budget-Friendly**")
                            st.write("Affordable housing segment")
                    
                    with col3:
                        st.markdown("#### 🏘️ **Property Type Analysis**")
                        if bhk >= 4:
                            st.success("**Family Home**")
                            st.write("Large family accommodation")
                        elif bhk == 3:
                            st.info("**Standard Family**")
                            st.write("Typical family size property")
                        else:
                            st.warning("**Compact Living**")
                            st.write("Small family or investment property")
                    
                    # Market comparison
                    try:
                        location_data = data[data['location'] == location]
                        if not location_data.empty:
                            st.markdown("### 🏆 Market Comparison")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                location_avg = location_data['price'].mean()
                                price_diff = prediction - location_avg
                                price_diff_pct = (price_diff / location_avg) * 100
                                
                                # Format comparison price
                                comp_price_display = format_price(prediction)
                                
                                st.metric(
                                    "vs Area Average", 
                                    comp_price_display,
                                    f"{price_diff_pct:+.1f}%"
                                )
                            
                            with col2:
                                overall_avg = data['price'].mean()
                                overall_diff = prediction - overall_avg
                                overall_diff_pct = (overall_diff / overall_avg) * 100
                                
                                st.metric(
                                    "vs City Average", 
                                    comp_price_display,
                                    f"{overall_diff_pct:+.1f}%"
                                )
                    except:
                        pass
                    
                except Exception as e:
                    st.error(f"Error making prediction: {e}")
                    st.info("Using fallback prediction method...")
                    prediction = simple_predict(location, sqft, bath, bhk, data)
                    # Format fallback prediction
                    fallback_display = format_price(prediction)
                    
                    st.success(f"Fallback prediction: {fallback_display}")
        else:
            st.warning("⚠️ Please fill in all the required fields!")

# Market insights section
st.markdown("---")
st.markdown("### 📊 **Detailed Market Insights**")

if location:
    try:
        location_data = data[data['location'] == location]
        
        if not location_data.empty:
            # Market statistics
            st.markdown("#### 📈 **Location Market Statistics**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_price = location_data['price'].mean()
                st.metric("💰 Average Price", format_price(avg_price))
            
            with col2:
                median_price = location_data['price'].median()
                st.metric("📊 Median Price", format_price(median_price))
            
            with col3:
                min_price = location_data['price'].min()
                st.metric("📉 Lowest Price", format_price(min_price))
            
            with col4:
                max_price = location_data['price'].max()
                st.metric("📈 Highest Price", format_price(max_price))
            
            # Market analysis
            st.markdown("#### 🎯 **Market Analysis**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💰 Price Range Analysis**")
                price_range = max_price - min_price
                price_range_formatted = format_price(price_range)
                
                if price_range >= 10000000:
                    st.success(f"**High Price Variation**: ₹{price_range/10000000:.2f} Cr range")
                    st.write("This area has diverse property types and sizes")
                elif price_range >= 5000000:
                    st.info(f"**Moderate Variation**: ₹{price_range/100000:.2f} L range")
                    st.write("Standard market with good variety")
                else:
                    st.warning(f"**Low Variation**: ₹{price_range/100000:.2f} L range")
                    st.write("Consistent pricing in this area")
                
                # Price per sq ft analysis
                avg_price_per_sqft = avg_price / location_data['total_sqft'].mean()
                st.markdown("**📐 Average Price per Sq Ft**")
                if avg_price_per_sqft >= 10000:
                    st.success(f"₹{avg_price_per_sqft/1000:.1f}K - Premium Area")
                elif avg_price_per_sqft >= 7000:
                    st.info(f"₹{avg_price_per_sqft/1000:.1f}K - Good Market")
                else:
                    st.warning(f"₹{avg_price_per_sqft/1000:.1f}K - Affordable Area")
            
            with col2:
                st.markdown("**🏘️ Property Distribution**")
                
                # BHK distribution
                bhk_counts = location_data['bhk'].value_counts().head(5)
                st.write("**BHK Distribution:**")
                for bhk, count in bhk_counts.items():
                    percentage = (count / len(location_data)) * 100
                    st.write(f"• {bhk} BHK: {count} properties ({percentage:.1f}%)")
                
                # Size analysis
                avg_size = location_data['total_sqft'].mean()
                st.markdown("**📏 Average Property Size**")
                st.write(f"**{avg_size:.0f} sq ft** - Typical property size in this area")
                
                if avg_size >= 2000:
                    st.success("Large properties dominate this area")
                elif avg_size >= 1200:
                    st.info("Medium-sized properties are common")
                else:
                    st.warning("Compact properties are typical here")
            
            # Charts
            st.markdown("#### 📊 **Market Visualizations**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💰 Price Distribution**")
                try:
                    # Create price bins for better visualization
                    price_bins = pd.cut(location_data['price'], bins=8)
                    price_dist = price_bins.value_counts().sort_index()
                    st.bar_chart(price_dist)
                except:
                    st.bar_chart(location_data['price'].head(50))
            
            with col2:
                st.markdown("**📐 Size vs Price Relationship**")
                try:
                    chart_data = location_data[['total_sqft', 'price']].head(100)
                    st.scatter_chart(chart_data, x='total_sqft', y='price')
                except:
                    st.line_chart(location_data[['total_sqft', 'price']].head(50))
            
            # Market recommendations
            st.markdown("#### 💡 **Market Recommendations**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 For Buyers**")
                if avg_price_per_sqft >= 12000:
                    st.info("• Premium area - expect higher prices")
                    st.info("• Good for long-term investment")
                    st.info("• High resale value potential")
                elif avg_price_per_sqft >= 8000:
                    st.success("• Balanced market with good options")
                    st.success("• Suitable for both living and investment")
                    st.success("• Stable appreciation expected")
                else:
                    st.warning("• Affordable area with good value")
                    st.warning("• Great for first-time buyers")
                    st.warning("• Potential for future appreciation")
            
            with col2:
                st.markdown("**📈 For Investors**")
                if len(location_data) >= 100:
                    st.success("• High market activity")
                    st.success("• Good liquidity for resale")
                    st.success("• Strong rental demand potential")
                elif len(location_data) >= 50:
                    st.info("• Moderate market activity")
                    st.info("• Steady investment potential")
                    st.info("• Balanced risk-reward")
                else:
                    st.warning("• Limited market data")
                    st.warning("• Higher investment risk")
                    st.warning("• Consider other areas for comparison")
        
        else:
            st.info("No data available for this location")
    except Exception as e:
        st.error(f"Error loading market insights: {e}")

# Sidebar with additional information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **Bengaluru House Price Predictor**
    
    This application uses machine learning to predict house prices in Bengaluru based on:
    - 📍 Location
    - 🏠 Number of BHK
    - 🚿 Number of bathrooms
    - 📏 Square footage
    
    **Model:** Ridge Regression with location encoding
    """)
    
    st.header("📊 Dataset Statistics")
    st.write(f"📈 Total properties: {len(data):,}")
    st.write(f"🏘️ Number of locations: {len(locations)}")
    # Format price range in lakhs/crores
    min_price = data['price'].min()
    max_price = data['price'].max()
    
    if min_price >= 10000000:
        min_price_display = f"₹{min_price/10000000:.2f} Cr"
    elif min_price >= 100000:
        min_price_display = f"₹{min_price/100000:.2f} L"
    else:
        min_price_display = f"₹{min_price:,.0f}"
    
    if max_price >= 10000000:
        max_price_display = f"₹{max_price/10000000:.2f} Cr"
    elif max_price >= 100000:
        max_price_display = f"₹{max_price/100000:.2f} L"
    else:
        max_price_display = f"₹{max_price:,.0f}"
    
    st.write(f"💰 Price range: {min_price_display} - {max_price_display}")
    st.write(f"📐 Size range: {data['total_sqft'].min():,.0f} - {data['total_sqft'].max():,.0f} sq ft")
    
    # Top locations by average price
    st.subheader("🏆 Top 10 Expensive Areas")
    try:
        top_locations = data.groupby('location')['price'].mean().sort_values(ascending=False).head(10)
        for i, (loc, price) in enumerate(top_locations.items(), 1):
            if price >= 10000000:
                price_display = f"₹{price/10000000:.2f} Cr"
            elif price >= 100000:
                price_display = f"₹{price/100000:.2f} L"
            else:
                price_display = f"₹{price:,.0f}"
            st.write(f"{i}. **{loc}**: {price_display}")
    except:
        st.info("Data not available")
    
    # Bottom locations
    st.subheader("💡 Most Affordable Areas")
    try:
        bottom_locations = data.groupby('location')['price'].mean().sort_values().head(10)
        for i, (loc, price) in enumerate(bottom_locations.items(), 1):
            if price >= 10000000:
                price_display = f"₹{price/10000000:.2f} Cr"
            elif price >= 100000:
                price_display = f"₹{price/100000:.2f} L"
            else:
                price_display = f"₹{price:,.0f}"
            st.write(f"{i}. **{loc}**: {price_display}")
    except:
        st.info("Data not available")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Built by Gagandeep using Stramlit</p>
</div>
""", unsafe_allow_html=True)
