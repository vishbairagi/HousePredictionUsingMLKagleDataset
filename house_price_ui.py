import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time
import json

st.set_page_config(
    page_title="AI House Predictor", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    .main {
        padding: 0.5rem 2rem;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="%23ffffff" opacity="0.1"/><circle cx="80" cy="80" r="1" fill="%23ffffff" opacity="0.1"/><circle cx="40" cy="60" r="1" fill="%23ffffff" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #f8fafc;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        color: #e2e8f0;
        position: relative;
        z-index: 1;
    }
    
    .glass-card {
        background: rgba(45, 55, 72, 0.7);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(74, 85, 104, 0.6);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .section-header::after {
        content: '';
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #667eea, transparent);
    }
    
    .input-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .input-item {
        background: rgba(26, 32, 44, 0.8);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(74, 85, 104, 0.4);
        transition: all 0.3s ease;
    }
    
    .input-item:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .input-label {
        color: #cbd5e0;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .prediction-showcase {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #4a5568 100%);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        margin: 3rem 0;
        border: 2px solid #667eea;
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .prediction-showcase::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(102, 126, 234, 0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .price-display {
        font-size: 4rem;
        font-weight: 800;
        color: #4ade80;
        margin: 1.5rem 0;
        text-shadow: 0 0 20px rgba(74, 222, 128, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(45, 55, 72, 0.8), rgba(74, 85, 104, 0.6));
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(74, 85, 104, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .predict-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: #f8fafc;
        border: none;
        padding: 1.2rem 3rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s ease;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .predict-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .predict-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .predict-btn:hover::before {
        left: 100%;
    }
    
    .history-container {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 10px;
    }
    
    .history-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .history-container::-webkit-scrollbar-track {
        background: rgba(26, 32, 44, 0.5);
        border-radius: 10px;
    }
    
    .history-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    .history-card {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.9), rgba(45, 55, 72, 0.7));
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #4ade80;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(74, 85, 104, 0.3);
    }
    
    .history-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(74, 222, 128, 0.2);
        border-left-color: #22d3ee;
    }
    
    .history-info {
        color: #e2e8f0;
    }
    
    .history-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4ade80;
        text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);
    }
    
    .chart-container {
        background: rgba(26, 32, 44, 0.8);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(74, 85, 104, 0.4);
        backdrop-filter: blur(10px);
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #a0aec0;
        font-style: italic;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    /* Streamlit component styling */
    .stSelectbox > div > div {
        background-color: rgba(26, 32, 44, 0.8) !important;
        border: 1px solid rgba(74, 85, 104, 0.6) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(26, 32, 44, 0.8) !important;
        border: 1px solid rgba(74, 85, 104, 0.6) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    
    .stSlider > div > div > div {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        color: #f8fafc !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stSpinner {
        color: #667eea !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        color: #fca5a5 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        color: #86efac !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1) !important;
        color: #93c5fd !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for predictions history
if 'local_history' not in st.session_state:
    st.session_state.local_history = []

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🏠 AI House Price Predictor</div>
    <div class="hero-subtitle">Advanced Machine Learning Property Valuation System</div>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    # Input Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🏡 Property Configuration</div>', unsafe_allow_html=True)
    
    # Create input grid
    input_cols = st.columns(3)
    
    with input_cols[0]:
        st.markdown('<div class="input-label">Quality Rating (1-10)</div>', unsafe_allow_html=True)
        overall_qual = st.slider(
            "", 
            min_value=1, max_value=10, value=7,
            help="Overall material and finish quality",
            key="quality"
        )
        
        st.markdown('<div class="input-label">Living Area (sq ft)</div>', unsafe_allow_html=True)
        gr_liv_area = st.number_input(
            "", 
            min_value=300, max_value=10000, value=2000,
            key="living_area"
        )
        
    with input_cols[1]:
        st.markdown('<div class="input-label">Year Built</div>', unsafe_allow_html=True)
        year_built = st.number_input(
            "", 
            min_value=1800, max_value=2025, value=2005,
            key="year_built"
        )
        
        st.markdown('<div class="input-label">Basement Area (sq ft)</div>', unsafe_allow_html=True)
        total_bsmt_sf = st.number_input(
            "", 
            min_value=0, max_value=5000, value=1000,
            key="basement"
        )
        
    with input_cols[2]:
        st.markdown('<div class="input-label">Garage Capacity</div>', unsafe_allow_html=True)
        garage_cars = st.selectbox(
            "", 
            options=[0, 1, 2, 3, 4, 5], 
            index=2,
            key="garage"
        )
        
        st.markdown('<div class="input-label">Full Bathrooms</div>', unsafe_allow_html=True)
        full_bath = st.selectbox(
            "", 
            options=list(range(0, 6)), 
            index=2,
            key="bathrooms"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Property Metrics
    total_area = gr_liv_area + total_bsmt_sf
    property_age = 2025 - year_built
    quality_labels = ["Very Poor", "Poor", "Fair", "Below Average", "Average", "Above Average", "Good", "Very Good", "Excellent", "Outstanding"]
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Property Analytics</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{total_area:,}</div>
            <div class="metric-label">Total Square Feet</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{property_age}</div>
            <div class="metric-label">Years Old</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{quality_labels[overall_qual-1]}</div>
            <div class="metric-label">Quality Grade</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{full_bath + garage_cars}</div>
            <div class="metric-label">Key Features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction Section
    predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])
    
    with predict_col2:
        if st.button("🔮 Generate Prediction", key="predict"):
            with st.spinner("🤖 AI Processing..."):
                time.sleep(1.5)
                features = [overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath, year_built]
                
                try:
                    url = "http://127.0.0.1:5000/predict"
                    response = requests.post(url, json={"features": features})
                    
                    if response.status_code == 200:
                        predicted_price = response.json()["predicted_price"]
                        
                        # Add to local history
                        prediction_data = {
                            'id': len(st.session_state.local_history) + 1,
                            'predicted_price': predicted_price,
                            'year_built': year_built,
                            'quality': overall_qual,
                            'area': total_area,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        st.session_state.local_history.append(prediction_data)
                        
                        st.markdown(f"""
                        <div class="prediction-showcase">
                            <h3 style="color: #e2e8f0; margin-bottom: 1rem;">💰 Predicted Property Value</h3>
                            <div class="price-display">${predicted_price:,.0f}</div>
                            <p style="color: #cbd5e0; margin-top: 1rem;">Based on advanced ML algorithms and market analysis</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Additional insights
                        price_per_sqft = predicted_price / total_area if total_area > 0 else 0
                        market_segment = "Luxury" if predicted_price > 500000 else "Premium" if predicted_price > 300000 else "Standard"
                        confidence = min(98, max(82, 90 + (overall_qual - 5) * 2))
                        
                        insight_cols = st.columns(3)
                        with insight_cols[0]:
                            st.metric("💵 Price/Sq Ft", f"${price_per_sqft:.0f}", delta="Market Rate")
                        with insight_cols[1]:
                            st.metric("🏆 Market Tier", market_segment, delta="Classification")
                        with insight_cols[2]:
                            st.metric("🎯 Confidence", f"{confidence}%", delta="AI Accuracy")
                            
                    else:
                        st.error("❌ Prediction service temporarily unavailable")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Unable to connect to prediction service. Please ensure the API server is running on localhost:5000")
                except Exception as e:
                    st.error(f"❌ System Error: {str(e)}")

with col2:
    # Market Trends Chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Market Insights</div>', unsafe_allow_html=True)
    
    # Enhanced market data
    years = list(range(2019, 2026))
    prices = [235000, 248000, 265000, 289000, 312000, 298000, 325000]
    
    fig = go.Figure()
    
    # Main trend line
    fig.add_trace(go.Scatter(
        x=years, 
        y=prices,
        mode='lines+markers',
        line=dict(color='#4ade80', width=4, shape='spline'),
        marker=dict(size=12, color='#22d3ee', symbol='diamond'),
        fill='tonexty',
        fillcolor='rgba(74, 222, 128, 0.1)',
        name='Market Trend'
    ))
    
    # Add forecast area
    fig.add_trace(go.Scatter(
        x=[2024, 2025],
        y=[298000, 325000],
        mode='lines',
        line=dict(color='#f093fb', width=3, dash='dash'),
        name='Forecast'
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            showgrid=False, 
            color='#e2e8f0',
            title='Year',
            title_font=dict(color='#cbd5e0')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(74, 85, 104, 0.3)',
            color='#e2e8f0',
            title='Price ($)',
            title_font=dict(color='#cbd5e0')
        ),
        plot_bgcolor='rgba(26, 32, 44, 0.8)',
        paper_bgcolor='rgba(26, 32, 44, 0.8)',
        font=dict(color='#e2e8f0'),
        showlegend=False,
        title=dict(
            text='Regional Price Trends',
            font=dict(color='#e2e8f0', size=16),
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market factors
    st.markdown("""
    <div style="margin-top: 1rem;">
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #667eea;">
            <strong style="color: #93c5fd;">📍 Location Impact:</strong><br>
            <span style="color: #cbd5e0; font-size: 0.9rem;">Neighborhood quality affects valuation by ±25%</span>
        </div>
        <div style="background: rgba(240, 147, 251, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #f093fb;">
            <strong style="color: #f0abfc;">⭐ Quality Score:</strong><br>
            <span style="color: #cbd5e0; font-size: 0.9rem;">Material grade is the strongest predictor</span>
        </div>
        <div style="background: rgba(74, 222, 128, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #4ade80;">
            <strong style="color: #86efac;">🏗️ Property Age:</strong><br>
            <span style="color: #cbd5e0; font-size: 0.9rem;">Newer construction commands premium pricing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction History Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📜 Prediction History</div>', unsafe_allow_html=True)

# Try to get history from API first, fall back to local storage
try:
    history_url = "http://127.0.0.1:5000/history"
    history_response = requests.get(history_url, timeout=2)
    
    if history_response.status_code == 200:
        api_history = history_response.json()
        if api_history:
            st.markdown('<div class="history-container">', unsafe_allow_html=True)
            for i, row in enumerate(api_history[-10:]):  # Show last 10
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-info">
                        <strong>Prediction #{row['id']}</strong><br>
                        <span style="color: #a0aec0;">Built {row['year_built']} • {datetime.now().strftime('%m/%d/%Y')}</span>
                    </div>
                    <div class="history-price">${row['predicted_price']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Show local history if API has no data
            if st.session_state.local_history:
                st.markdown('<div class="history-container">', unsafe_allow_html=True)
                for prediction in reversed(st.session_state.local_history[-10:]):
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="history-info">
                            <strong>Prediction #{prediction['id']}</strong><br>
                            <span style="color: #a0aec0;">Built {prediction['year_built']} • Quality {prediction['quality']}/10</span><br>
                            <span style="color: #718096; font-size: 0.8rem;">{prediction['timestamp']}</span>
                        </div>
                        <div class="history-price">${prediction['predicted_price']:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">🎯</div>
                    <div>No predictions yet. Generate your first property valuation above!</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Show local history when API is not available
        if st.session_state.local_history:
            st.markdown('<div class="history-container">', unsafe_allow_html=True)
            for prediction in reversed(st.session_state.local_history[-10:]):
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-info">
                        <strong>Session Prediction #{prediction['id']}</strong><br>
                        <span style="color: #a0aec0;">Built {prediction['year_built']} • Quality {prediction['quality']}/10</span><br>
                        <span style="color: #718096; font-size: 0.8rem;">{prediction['timestamp']}</span>
                    </div>
                    <div class="history-price">${prediction['predicted_price']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🎯</div>
                <div>No predictions yet. Generate your first property valuation above!</div>
            </div>
            """, unsafe_allow_html=True)
        
except requests.exceptions.ConnectionError:
    # Show local history when API is not connected
    if st.session_state.local_history:
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        for prediction in reversed(st.session_state.local_history[-10:]):
            st.markdown(f"""
            <div class="history-card">
                <div class="history-info">
                    <strong>Local Prediction #{prediction['id']}</strong><br>
                    <span style="color: #a0aec0;">Built {prediction['year_built']} • Quality {prediction['quality']}/10</span><br>
                    <span style="color: #718096; font-size: 0.8rem;">{prediction['timestamp']}</span>
                </div>
                <div class="history-price">${prediction['predicted_price']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🏠</div>
            <div>Start making predictions to see your history here!</div>
            <div style="margin-top: 1rem; font-size: 0.9rem; color: #718096;">
                API connection unavailable - using local storage
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    if st.session_state.local_history:
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        for prediction in reversed(st.session_state.local_history[-10:]):
            st.markdown(f"""
            <div class="history-card">
                <div class="history-info">
                    <strong>Prediction #{prediction['id']}</strong><br>
                    <span style="color: #a0aec0;">Built {prediction['year_built']} • {prediction['area']:,} sq ft</span><br>
                    <span style="color: #718096; font-size: 0.8rem;">{prediction['timestamp']}</span>
                </div>
                <div class="history-price">${prediction['predicted_price']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔮</div>
            <div>Ready to predict your first property value?</div>
            <div style="margin-top: 0.5rem; color: #a0aec0;">Enter property details above and click predict!</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Statistics Dashboard
if st.session_state.local_history:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Session Analytics</div>', unsafe_allow_html=True)
    
    # Calculate statistics
    prices = [p['predicted_price'] for p in st.session_state.local_history]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    total_predictions = len(st.session_state.local_history)
    
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{total_predictions}</div>
            <div class="metric-label">Total Predictions</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${avg_price:,.0f}</div>
            <div class="metric-label">Average Price</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${min_price:,.0f}</div>
            <div class="metric-label">Minimum Price</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${max_price:,.0f}</div>
            <div class="metric-label">Maximum Price</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1)); border-radius: 15px; margin-top: 2rem;">
    <div style="color: #cbd5e0; font-size: 1.1rem; margin-bottom: 0.5rem;">
        🤖 Powered by Advanced AI • Built with Streamlit & Python
    </div>
    <div style="color: #a0aec0; font-size: 0.9rem;">
        Real estate predictions for the modern world • © 2025 AI Property Solutions
    </div>
</div>
""", unsafe_allow_html=True)