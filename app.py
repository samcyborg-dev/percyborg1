import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np

# Page config
st.set_page_config(page_title="Cyborg Trader Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1f77b4; text-align: center;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 1rem; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Sidebar: Controls
st.sidebar.header("🚀 Cyborg Controls")
upload_csv = st.sidebar.file_uploader("Upload Portfolio CSV", type=['csv'])
risk_limit_dd = st.sidebar.slider("Max Drawdown %", -5, -30, -20)
risk_limit_daily = st.sidebar.slider("Daily Loss %", -2, -10, -5)

# Main Header
st.markdown('<h1 class="main-header">🦾 Samson Fernando Cyborg Dashboard</h1>', unsafe_allow_html=True)

# Row 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)
if upload_csv:
    df = pd.read_csv(upload_csv)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
    
    current_equity = df['Equity'].iloc[-1]
    current_dd = df['Drawdown'].min()
    sharpe = df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252)
    
    col1.metric("Current Equity", f"${current_equity:,.0f}", delta="+$2.1k")
    col2.metric("Max Drawdown", f"{current_dd:.1f}%", delta="+1.2%")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}", delta="+0.08")
    col4.metric("Regime", "Choppy", delta="Vol ↓")
else:
    # Demo data
    col1.metric("Current Equity", "$125,342", delta="+$2.1k")
    col2.metric("Max Drawdown", "-14.3%", delta="+1.2%")
    col3.metric("Sharpe Ratio", "1.18", delta="+0.08")
    col4.metric("Regime", "Choppy", delta="Vol ↓")

# Row 2: Charts
col_left, col_right = st.columns([2,1])

with col_left:
    st.subheader("📈 Equity Curve + Drawdown")
    
    # Demo chart data (replace with CSV)
    dates = pd.date_range('2026-01-01', periods=90)
    equity = 100000 * np.exp(np.cumsum(np.random.normal(0.0005, 0.01, 90)))
    drawdown = (equity / np.maximum.accumulate(equity) - 1) * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=dates, y=equity, name='Equity', line=dict(color='#1f77b4')), secondary_y=False)
    fig.add_trace(go.Scatter(x=dates, y=drawdown, name='Drawdown', line=dict(color='#ef5532')), secondary_y=True)
    fig.update_layout(height=400, title="Live Portfolio Performance")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("⚠️ Risk Status")
    
    risk_data = pd.DataFrame({
        'Metric': ['Open Risk', 'Max Pos', 'Volatility', 'Sharpe', 'Drawdown'],
        'Current': [8.2, 2.1, 12.5, 1.18, -14.3],
        'Limit': [10.0, 3.0, 15.0, 1.0, risk_limit_dd],
        'Status': ['🟢', '🟢', '🟢', '🟢', '🟡']
    })
    
    st.dataframe(risk_data, use_container_width=True)

# Row 3: Strategy Attribution
st.subheader("📊 Strategy Performance")
strategies_df = pd.DataFrame({
    'Strategy': ['S1 MeanRev', 'S2 Trend', 'S3 Hedge', 'S4 Event'],
    'Return': [2.1, -0.8, 4.7, 0.9],
    'Risk %': [38, 32, 15, 15],
    'Sharpe': [1.42, 0.67, 0.89, 1.12],
    'Status': ['✅ Core', '⚠️ Trial', '✅ Core', '🆕 Trial']
})

fig_bar = go.Figure(data=[
    go.Bar(name='Return', x=strategies_df['Strategy'], y=strategies_df['Return'], marker_color='#1f77b4'),
    go.Bar(name='Risk', x=strategies_df['Strategy'], y=strategies_df['Risk %'], marker_color='#ff7f0e', yaxis='y2')
])
fig_bar.update_layout(title='Strategy Attribution', yaxis=dict(title='Return %'), yaxis2=dict(title='Risk %', overlaying='y', side='right'))
st.plotly_chart(fig_bar, use_container_width=True)

# Row 4: GitHub Screener Integration
st.subheader("🔍 GitHub Quant Screener")
if st.button("Run Screener"):
    st.success("✅ Top repo: freqtrade/freqtrade (Quant Score: 95)")
    st.info("Deploy: `docker run freqtrade/freqtrade`")

st.code("""
docker run -d --name cyborg-bot \\
  -v /data:/app/data \\
  freqtrade/freqtrade:latest
""")

# Row 5: Cyborg Status
st.subheader("🤖 Cyborg Status")
col1, col2, col3 = st.columns(3)
col1.metric("Autonomy Level", "Level 2/4", "→ Level 3")
col2.metric("Agents Active", "4/6", "+1 Risk Agent")
col3.metric("Next Review", "Mar 30, 2026", "24h")

# Footer
st.markdown("---")
st.markdown("*Built for Samson Fernando | Top 0.01% Cyborg Trader | March 2026*")
