import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SolCool Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================
BG = "#F5F3ED"
CARD = "#FFFFFF"
INK = "#173B2C"
INK_2 = "#28533E"
MUTED = "#68756E"
BORDER = "#DDE4DE"
GRID = "#E8EDE9"
GREEN = "#2E7D5B"
GREEN_LIGHT = "#E8F3EC"
AMBER = "#D79B24"
RED = "#C95B52"
BLUE = "#4D7EA8"
PURPLE = "#7A67A8"

# ============================================================
# PROFESSIONAL UI CSS
# ============================================================
st.markdown(
    f'''
    <style>
    /* ---------- App ---------- */
    .stApp {{ background: {BG}; }}
    .main {{ background: {BG}; }}
    .block-container {{
        max-width: 1500px;
        padding-top: 2.0rem;
        padding-bottom: 3.5rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
    }}

    /* ---------- Typography ---------- */
    h1 {{
        color: {INK} !important;
        font-size: 38px !important;
        line-height: 1.12 !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px !important;
    }}
    h2 {{
        color: {INK} !important;
        font-size: 27px !important;
        font-weight: 750 !important;
        letter-spacing: -0.35px !important;
    }}
    h3 {{
        color: {INK_2} !important;
        font-size: 19px !important;
        font-weight: 700 !important;
    }}
    p, .stCaption {{ color: {MUTED}; }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #173B2C 0%, #123225 100%);
        border-right: 1px solid #28533E;
    }}
    section[data-testid="stSidebar"] * {{ color: #F7FBF8 !important; }}
    section[data-testid="stSidebar"] .stRadio label {{
        font-size: 14px;
        font-weight: 600;
    }}
    section[data-testid="stSidebar"] .stRadio > div {{ gap: 7px; }}
    section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.16); }}

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stTextInput"] > div {{
        border-radius: 10px;
    }}
    .stSlider [data-baseweb="slider"] {{ padding-top: 3px; }}

    /* ---------- Buttons ---------- */
    .stButton > button {{
        width: 100%;
        min-height: 44px;
        border: 0;
        border-radius: 11px;
        background: linear-gradient(135deg, #173B2C, #2E6B50);
        color: white;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(23,59,44,.16);
        transition: all .18s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        background: linear-gradient(135deg, #28533E, #367C5D);
        box-shadow: 0 8px 18px rgba(23,59,44,.22);
    }}

    /* ---------- Native metric cards ---------- */
    div[data-testid="stMetric"] {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 17px 18px 15px 18px;
        box-shadow: 0 5px 18px rgba(23,59,44,.055);
        min-height: 112px;
    }}
    div[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
    div[data-testid="stMetricValue"] {{ color: {INK}; font-weight: 800; }}

    /* ---------- Chart cards ---------- */
    div[data-testid="stPlotlyChart"] {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 7px 7px 3px 7px;
        box-shadow: 0 7px 24px rgba(23,59,44,.055);
        overflow: hidden;
    }}

    /* ---------- Dataframe ---------- */
    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(23,59,44,.045);
    }}

    /* ---------- Custom cards ---------- */
    .hero {{
        background: linear-gradient(135deg, #173B2C 0%, #28533E 60%, #326A50 100%);
        border-radius: 20px;
        padding: 31px 34px;
        margin: 0 0 24px 0;
        box-shadow: 0 12px 32px rgba(23,59,44,.14);
        position: relative;
        overflow: hidden;
    }}
    .hero:after {{
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        right: -90px;
        top: -100px;
        background: rgba(255,255,255,.07);
    }}
    .hero-title {{ color:#fff; font-size:34px; font-weight:800; margin-bottom:8px; position:relative; z-index:1; }}
    .hero-text {{ color:#DCE9E0; font-size:15px; line-height:1.6; max-width:850px; position:relative; z-index:1; }}

    .section-note {{
        background: #EEF4EF;
        border: 1px solid #DCE8DE;
        border-radius: 12px;
        padding: 12px 15px;
        color: #4E6257;
        font-size: 13px;
        margin: 5px 0 14px 0;
    }}
    .decision-store {{
        background: linear-gradient(135deg,#E8F5EC,#F5FBF7);
        border: 1px solid #B9DCC2;
        border-radius: 17px;
        padding: 27px;
        text-align:center;
        box-shadow: 0 8px 22px rgba(46,125,91,.10);
    }}
    .decision-sell {{
        background: linear-gradient(135deg,#FCEBE9,#FFF7F6);
        border: 1px solid #E7B9B6;
        border-radius: 17px;
        padding: 27px;
        text-align:center;
        box-shadow: 0 8px 22px rgba(201,91,82,.08);
    }}
    .decision-title {{ font-size:26px; font-weight:800; color:{INK}; }}
    .decision-text {{ font-size:14px; margin-top:8px; color:{MUTED}; }}
    .footer {{ text-align:center; padding-top:30px; color:#7A847E; font-size:12px; }}

    @media (max-width: 900px) {{
        .block-container {{ padding-left:1rem; padding-right:1rem; }}
        h1 {{ font-size:31px !important; }}
    }}
    </style>
    ''',
    unsafe_allow_html=True,
)

# ============================================================
# DATA / MODELS
# ============================================================
@st.cache_data
def load_data():
    data = pd.read_csv("data/solcool_data.csv")
    data["date"] = pd.to_datetime(data["date"])
    return data

@st.cache_resource
def load_models():
    demand_model = joblib.load("models/demand_model.pkl")
    risk_model = joblib.load("models/spoilage_model.pkl")
    return demand_model, risk_model

df = load_data()
demand_model, risk_model = load_models()

# ============================================================
# PLOTLY DESIGN SYSTEM
# ============================================================
PLOTLY_COLORS = [GREEN, BLUE, AMBER, PURPLE, RED, "#6F9E82"]
RISK_COLORS = {"LOW": GREEN, "MEDIUM": AMBER, "HIGH": RED}


def style_chart(fig, height=410, showlegend=True):
    '''Apply one consistent, readable SolCool visual system to every Plotly chart.'''
    fig.update_layout(
        height=height,
        template=None,
        paper_bgcolor=CARD,
        plot_bgcolor="#FBFCFB",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=12),
        colorway=PLOTLY_COLORS,
        hoverlabel=dict(
            bgcolor=INK,
            bordercolor=INK,
            font=dict(color="white", size=12),
        ),
        margin=dict(l=55, r=25, t=28, b=55),
        showlegend=showlegend,
        legend=dict(
            bgcolor="rgba(255,255,255,.88)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=INK, size=11),
        ),
        title=dict(font=dict(color=INK, size=16)),
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor="#C9D2CB",
        linewidth=1,
        ticks="outside",
        tickcolor="#AEB9B1",
        tickfont=dict(color=MUTED, size=11),
        title_font=dict(color=INK_2, size=12),
        zeroline=False,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        gridwidth=1,
        showline=False,
        ticks="outside",
        tickcolor="#AEB9B1",
        tickfont=dict(color=MUTED, size=11),
        title_font=dict(color=INK_2, size=12),
        zeroline=False,
    )
    return fig


def show_chart(fig, height=410, key=None):
    fig = style_chart(fig, height=height)
    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
        key=key,
    )

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown(
    '''
    <div style="font-size:28px;font-weight:800;margin-bottom:3px;">🌱 SolCool</div>
    <div style="font-size:13px;color:#DCE9E0;margin-bottom:22px;">Cold Storage Intelligence</div>
    ''',
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Dashboard",
    ["Overview", "Demand Forecast", "Spoilage Risk", "FPO Analytics", "Economics", "Decision Engine"],
)
st.sidebar.divider()
st.sidebar.caption("ML-powered decision support")
st.sidebar.caption("Synthetic demonstration dataset")

# ============================================================
# OVERVIEW
# ============================================================
if page == "Overview":
    st.markdown(
        '''
        <div class="hero">
            <div class="hero-title">SolCool ML Dashboard</div>
            <div class="hero-text">
                Data-driven decision support for decentralized solar-powered cold storage —
                combining demand forecasting, spoilage-risk prediction and farm-level analytics.
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    total_records = len(df)
    total_fpos = df["fpo"].nunique()
    avg_utilization = df["utilization_pct"].mean()
    high_risk = (df["spoilage_risk"] == "HIGH").sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TOTAL RECORDS", f"{total_records:,}", "Operational observations")
    c2.metric("FPO NETWORK", f"{total_fpos}", "Farmer Producer Organisations")
    c3.metric("AVG UTILIZATION", f"{avg_utilization:.1f}%", "Cold-storage capacity used")
    c4.metric("HIGH RISK CASES", f"{high_risk:,}", "Potential high-spoilage observations")

    st.markdown('<div class="section-note">📊 <b>Network snapshot:</b> Explore demand, risk and economics below. Hover over any chart for detailed values.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Storage Demand Distribution")
        fig = px.histogram(
            df, x="storage_demand_kg", nbins=35,
            labels={"storage_demand_kg": "Storage Demand (kg)"},
        )
        fig.update_traces(marker_color=GREEN, marker_line_color="white", marker_line_width=0.6, opacity=.9)
        fig.update_layout(xaxis_title="Storage Demand (kg)", yaxis_title="Number of observations")
        show_chart(fig, 400, "overview_demand_distribution")

    with c2:
        st.subheader("Spoilage Risk Distribution")
        risk_counts = df["spoilage_risk"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0).reset_index()
        risk_counts.columns = ["Risk Level", "Cases"]
        fig = px.bar(risk_counts, x="Risk Level", y="Cases", text="Cases", color="Risk Level", color_discrete_map=RISK_COLORS)
        fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
        fig.update_layout(xaxis_title="Risk level", yaxis_title="Cases", showlegend=False)
        show_chart(fig, 400, "overview_risk_distribution")

    st.subheader("Produce-Level Storage Demand")
    produce_summary = (
        df.groupby("produce")
        .agg(Average_Demand=("storage_demand_kg", "mean"), Average_Utilization=("utilization_pct", "mean"), Average_Price=("market_price", "mean"))
        .reset_index()
    )
    fig = px.bar(
        produce_summary.sort_values("Average_Demand", ascending=False),
        x="produce", y="Average_Demand", text_auto=".0f",
        color="Average_Demand", color_continuous_scale=["#DDEDE3", GREEN, INK],
        labels={"produce": "Produce", "Average_Demand": "Average Storage Demand (kg)"},
    )
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Produce", yaxis_title="Average demand (kg)")
    show_chart(fig, 430, "overview_produce_demand")

    st.subheader("Latest Operational Data")
    display_columns = ["date", "fpo", "produce", "harvest_volume_kg", "storage_demand_kg", "utilization_pct", "spoilage_risk", "market_price"]
    st.dataframe(df[display_columns].head(15), use_container_width=True, hide_index=True)

# ============================================================
# DEMAND FORECAST
# ============================================================
elif page == "Demand Forecast":
    st.title("Demand Forecast")
    st.caption("Use the trained Random Forest model to estimate required cold-storage capacity.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Input Conditions")
        temperature = st.slider("Temperature (°C)", 10.0, 50.0, 28.0, 0.5)
        humidity = st.slider("Humidity (%)", 20.0, 100.0, 65.0, 1.0)
        harvest = st.number_input("Harvest Volume (kg)", min_value=100, max_value=5000, value=1000, step=100)
    with c2:
        st.subheader("Storage Conditions")
        price = st.number_input("Current Market Price (₹/kg)", min_value=1.0, max_value=500.0, value=30.0, step=1.0)
        days = st.slider("Expected Storage Days", 1, 30, 5)
        capacity = st.number_input("Available Capacity (kg)", min_value=100, max_value=5000, value=1500, step=100)

    if st.button("Predict Storage Demand"):
        input_data = pd.DataFrame({
            "temperature": [temperature], "humidity": [humidity], "harvest_volume_kg": [harvest],
            "market_price": [price], "storage_days": [days], "storage_capacity_kg": [capacity],
        })
        prediction = float(demand_model.predict(input_data)[0])
        prediction = float(np.clip(prediction, 50, capacity))
        utilization = (prediction / capacity) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("PREDICTED DEMAND", f"{prediction:,.0f} kg")
        c2.metric("AVAILABLE CAPACITY", f"{capacity:,.0f} kg")
        c3.metric("EXPECTED UTILIZATION", f"{utilization:.1f}%")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=utilization,
            number={"suffix": "%", "font": {"color": INK, "size": 34}},
            title={"text": "Capacity Utilization", "font": {"color": INK_2, "size": 15}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": MUTED},
                "bar": {"color": GREEN},
                "bgcolor": "#EDF2EE",
                "bordercolor": BORDER,
                "borderwidth": 1,
                "steps": [{"range": [0, 70], "color": "#EEF7F1"}, {"range": [70, 90], "color": "#FFF5DD"}, {"range": [90, 100], "color": "#FDECE9"}],
                "threshold": {"line": {"color": RED, "width": 3}, "thickness": .8, "value": 90},
            },
        ))
        gauge.update_layout(height=310, paper_bgcolor=CARD, margin=dict(l=35, r=35, t=40, b=25), font=dict(color=INK))
        st.plotly_chart(gauge, use_container_width=True, theme=None, config={"displaylogo": False}, key="demand_gauge")

        if utilization > 90:
            st.error("Storage capacity may be insufficient under these conditions.")
        elif utilization > 70:
            st.warning("Storage capacity is expected to be well utilized.")
        else:
            st.success("Available storage capacity appears sufficient.")

# ============================================================
# SPOILAGE RISK
# ============================================================
elif page == "Spoilage Risk":
    st.title("Spoilage Risk Prediction")
    st.caption("Estimate produce spoilage risk using environmental and storage conditions.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Environmental Conditions")
        temperature = st.slider("Temperature (°C)", 10.0, 50.0, 28.0, 0.5)
        humidity = st.slider("Humidity (%)", 20.0, 100.0, 65.0, 1.0)
        storage_days = st.slider("Storage Days", 1, 30, 5)
    with c2:
        st.subheader("Storage Conditions")
        utilization = st.slider("Storage Utilization (%)", 0.0, 100.0, 60.0, 1.0)
        capacity = st.number_input("Storage Capacity (kg)", 100, 5000, 1500, 100)

    if st.button("Predict Spoilage Risk"):
        input_data = pd.DataFrame({
            "temperature": [temperature], "humidity": [humidity], "storage_days": [storage_days],
            "utilization_pct": [utilization], "storage_capacity_kg": [capacity],
        })
        prediction = risk_model.predict(input_data)[0]
        probabilities = risk_model.predict_proba(input_data)[0]
        classes = risk_model.classes_
        probability_df = pd.DataFrame({"Risk Level": classes, "Probability": probabilities * 100})

        badge_class = {"LOW": "decision-store", "MEDIUM": "decision-store", "HIGH": "decision-sell"}[prediction]
        icon = {"LOW": "🟢", "MEDIUM": "🟠", "HIGH": "🔴"}[prediction]
        st.markdown(
            f'''<div class="{badge_class}"><div class="decision-title">{icon} Predicted Risk: {prediction}</div><div class="decision-text">Model confidence is shown below across all three risk classes.</div></div>''',
            unsafe_allow_html=True,
        )
        st.write("")
        fig = px.bar(probability_df, x="Risk Level", y="Probability", text=probability_df["Probability"].round(1), color="Risk Level", color_discrete_map=RISK_COLORS)
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False, marker_line_width=0)
        fig.update_layout(xaxis_title="Risk level", yaxis_title="Model probability (%)", yaxis_range=[0, 105], showlegend=False)
        show_chart(fig, 400, "risk_probability_chart")

# ============================================================
# FPO ANALYTICS
# ============================================================
elif page == "FPO Analytics":
    st.title("FPO Analytics")
    st.caption("Compare storage utilization, demand and pricing across Farmer Producer Organisations.")

    selected_fpo = st.selectbox("Select FPO", sorted(df["fpo"].unique()))
    fpo_data = df[df["fpo"] == selected_fpo]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("RECORDS", f"{len(fpo_data):,}")
    c2.metric("AVG HARVEST", f"{fpo_data['harvest_volume_kg'].mean():,.0f} kg")
    c3.metric("AVG DEMAND", f"{fpo_data['storage_demand_kg'].mean():,.0f} kg")
    c4.metric("UTILIZATION", f"{fpo_data['utilization_pct'].mean():.1f}%")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Market Price vs Storage Demand")
        fig = px.scatter(
            fpo_data, x="market_price", y="storage_demand_kg", size="harvest_volume_kg",
            color="spoilage_risk", color_discrete_map=RISK_COLORS,
            hover_data=["produce", "storage_days", "utilization_pct"],
            labels={"market_price": "Market Price (₹/kg)", "storage_demand_kg": "Storage Demand (kg)"},
            size_max=34,
        )
        fig.update_traces(marker=dict(opacity=.78, line=dict(width=.7, color="white")))
        fig.update_layout(xaxis_title="Market price (₹/kg)", yaxis_title="Storage demand (kg)")
        show_chart(fig, 440, "fpo_price_demand")

    with c2:
        st.subheader("Average Demand by Produce")
        produce_fpo = fpo_data.groupby("produce")["storage_demand_kg"].mean().reset_index().sort_values("storage_demand_kg", ascending=False)
        fig = px.bar(produce_fpo, x="produce", y="storage_demand_kg", text_auto=".0f", color="storage_demand_kg", color_continuous_scale=["#DDEDE3", GREEN, INK], labels={"produce": "Produce", "storage_demand_kg": "Average Demand (kg)"})
        fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Produce", yaxis_title="Average demand (kg)")
        show_chart(fig, 440, "fpo_produce_demand")

    st.subheader("FPO Utilization by Produce")
    utilization_summary = fpo_data.groupby("produce")["utilization_pct"].mean().reset_index().sort_values("utilization_pct", ascending=False)
    fig = px.bar(utilization_summary, x="produce", y="utilization_pct", text=utilization_summary["utilization_pct"].round(1), color="utilization_pct", color_continuous_scale=["#DDEDE3", GREEN, INK], labels={"produce": "Produce", "utilization_pct": "Average Utilization (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False, marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, yaxis_range=[0, 105], xaxis_title="Produce", yaxis_title="Average utilization (%)")
    show_chart(fig, 400, "fpo_utilization")

# ============================================================
# ECONOMICS
# ============================================================
elif page == "Economics":
    st.title("Cold Storage Economics")
    st.caption("Estimate the revenue opportunity and storage economics represented by the dataset.")

    total_revenue = df["potential_revenue"].sum()
    total_storage_cost = (df["storage_demand_kg"] * df["storage_cost_per_kg"] * df["storage_days"]).sum()
    gross_value = total_revenue - total_storage_cost

    c1, c2, c3 = st.columns(3)
    c1.metric("POTENTIAL REVENUE", f"₹{total_revenue / 1e7:.2f} Cr")
    c2.metric("STORAGE COST", f"₹{total_storage_cost / 1e7:.2f} Cr")
    c3.metric("ESTIMATED GROSS VALUE", f"₹{gross_value / 1e7:.2f} Cr")

    economic_data = pd.DataFrame({"Metric": ["Potential Revenue", "Storage Cost", "Estimated Gross Value"], "Value": [total_revenue, total_storage_cost, gross_value]})
    fig = px.bar(economic_data, x="Metric", y="Value", text_auto=".2s", color="Metric", color_discrete_sequence=[GREEN, RED, BLUE], labels={"Value": "Value (₹)"})
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, xaxis_title="Economic metric", yaxis_title="Value (₹)")
    show_chart(fig, 430, "economics_summary")

    st.subheader("Economics by Produce")
    produce_economics = df.groupby("produce").agg(Revenue=("potential_revenue", "sum"), Storage_Cost=("storage_cost_per_kg", "mean")).reset_index().sort_values("Revenue", ascending=False)
    fig = px.bar(produce_economics, x="produce", y="Revenue", text_auto=".2s", color="Revenue", color_continuous_scale=["#DDEDE3", GREEN, INK], labels={"Revenue": "Potential Revenue (₹)"})
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Produce", yaxis_title="Potential revenue (₹)")
    show_chart(fig, 410, "economics_produce")

    st.subheader("Revenue Share by Produce")
    share = df.groupby("produce")["potential_revenue"].sum().reset_index()
    fig = px.pie(share, names="produce", values="potential_revenue", hole=.58, color_discrete_sequence=PLOTLY_COLORS)
    fig.update_traces(textposition="outside", textinfo="label+percent", marker=dict(line=dict(color="white", width=2)))
    fig.update_layout(height=440, paper_bgcolor=CARD, font=dict(family="Inter, Arial", color=INK), margin=dict(l=20,r=20,t=20,b=20), legend=dict(font=dict(color=INK)))
    st.plotly_chart(fig, use_container_width=True, theme=None, config={"displaylogo": False}, key="economics_share")

# ============================================================
# DECISION ENGINE
# ============================================================
elif page == "Decision Engine":
    st.title("SolCool Decision Engine")
    st.caption("A simple business rule combining expected market price appreciation with spoilage risk.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Market Conditions")
        current_price = st.number_input("Current Market Price (₹/kg)", 1.0, 500.0, 30.0, 1.0)
        future_price = st.number_input("Expected Future Price (₹/kg)", 1.0, 500.0, 40.0, 1.0)
    with c2:
        st.subheader("Storage Risk")
        risk = st.selectbox("Spoilage Risk", ["LOW", "MEDIUM", "HIGH"])

    price_growth = ((future_price - current_price) / current_price) * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("CURRENT PRICE", f"₹{current_price:.0f}/kg")
    c2.metric("EXPECTED PRICE", f"₹{future_price:.0f}/kg")
    c3.metric("EXPECTED INCREASE", f"{price_growth:.1f}%")

    if price_growth >= 10 and risk != "HIGH":
        st.markdown(
            '''<div class="decision-store"><div class="decision-title">🌱 RECOMMENDATION: STORE</div><div class="decision-text">Expected market appreciation is attractive and spoilage risk is manageable.</div></div>''',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '''<div class="decision-sell"><div class="decision-title">📦 RECOMMENDATION: SELL NOW</div><div class="decision-text">Expected price appreciation is insufficient or spoilage risk is too high.</div></div>''',
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("Decision Logic")
    logic_df = pd.DataFrame({
        "Condition": ["Expected price increase ≥ 10%", "Spoilage risk is not HIGH"],
        "Required": ["YES", "YES"],
    })
    st.dataframe(logic_df, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="footer">SolCool Analytics · ML Decision Support · Synthetic demonstration dataset</div>',
    unsafe_allow_html=True,
)
