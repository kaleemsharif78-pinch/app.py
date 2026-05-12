import streamlit as st
import math

# Page Configuration
st.set_page_config(page_title="NABA Solar Tech", page_icon="☀️")

# Branding Header
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>NABA SOLAR SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-weight: bold;'>OFFICIAL LOAD PLANNER</p>", unsafe_allow_html=True)
st.divider()

# --- SECTION 1: APPLIANCES ---
st.subheader("1. Appliances (Teadad Likhein)")
col1, col2 = st.columns(2)

with col1:
    f_p = st.number_input("Old Fans (100W) Qty", min_value=0, value=0)
    f_a = st.number_input("AC/DC Fans (65W) Qty", min_value=0, value=4)
    l_o = st.number_input("Normal Bulbs (60W) Qty", min_value=0, value=0)
    l_l = st.number_input("LED Bulbs (12W) Qty", min_value=0, value=10)

with col2:
    fr_q = st.number_input("Fridge Quantity", min_value=0, value=1)
    ac_q = st.number_input("AC Quantity", min_value=0, value=1)
    m_hp = st.number_input("Motor Power (HP)", min_value=0.0, value=1.0, step=0.5)
    m_q = st.number_input("Motor Quantity", min_value=0, value=1)

st.divider()

# --- SECTION 2: RATES & SPECS ---
st.subheader("2. Market Rates & System Specs")
col3, col4 = st.columns(2)

with col3:
    p_w = st.number_input("Solar Plate Watts (W)", min_value=1, value=585)
    p_r = st.number_input("Price Per Plate (Rs)", min_value=0, value=22000)
    inv_type = st.selectbox("Inverter Mode", ["Hybrid Inverter", "Off-Grid System"])

with col4:
    b_ah = st.number_input("Battery Capacity (Ah)", min_value=1, value=200)
    b_r = st.number_input("Price Per Battery (Rs)", min_value=0, value=45000)

# --- CALCULATION LOGIC ---
if st.button("GENERATE TECHNICAL REPORT", use_container_width=True):
    # Calculations
    motor_total_w = (m_hp * m_q * 746)
    fridge_load = (fr_q * 500)
    ac_load = (ac_q * 1500)
    fans_bulbs_load = (f_p*100) + (f_a*65) + (l_o*60) + (l_l*12)
    
    total_w = fans_bulbs_load + fridge_load + ac_load + motor_total_w
    kw = total_w / 1000
    
    # Solar Logic
    n_p = math.ceil((total_w * 1.30) / p_w)
    s_kw = math.ceil(kw + 1.5)
    
    # Battery Logic
    if s_kw <= 3: n_b, vol, conn = 2, 24, "1 String (2 Series)"
    elif s_kw <= 6: n_b, vol, conn = 4, 48, "1 String (4 Series)"
    else: n_b, vol, conn = 8, 48, "2 Strings (Parallel)"
    
    # Backup Logic
    night_load = fans_bulbs_load + (fr_q * 300)
    storage = (b_ah * vol * 0.8)
    hours = storage / night_load if night_load > 0 else 0
    
    # Display Results
    st.markdown(f"### 📊 Total Load: {int(total_w)}W ({kw:.2f} kW)")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.info(f"**Inverter:** {s_kw}kW ({vol}V)\n\nType: {inv_type}")
        st.success(f"**Solar Plates:** {n_p} Nos\n\nTotal: Rs. {n_p * p_r:,.0f}")
    
    with res_col2:
        st.info(f"**Batteries:** {n_b} Nos\n\n{conn}")
        st.success(f"**Battery Cost:**\n\nTotal: Rs. {n_b * b_r:,.0f}")
    
    st.warning(f"**Night Backup:** Approx {hours:.1f} Hours")
    st.error(f"## GRAND TOTAL: Rs. {(n_p * p_r) + (n_b * b_r):,.0f}")

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>NABA SOLUTIONS | PINCH BRAND © 2026</p>", unsafe_allow_html=True)
