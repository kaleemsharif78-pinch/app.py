import streamlit as st
import math

# Page Configuration
st.set_page_config(page_title="NABA Solar Tech", page_icon="☀️")

# Branding Header
st.markdown("<h1 style='text-align: center; color: #fbbf24; margin-bottom: 0;'>NABA SOLAR SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4ade80; font-size: 18px; font-weight: bold; margin-top: 0;'>Powered by NABA – Energy for Generations</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffffff; background-color: #1e293b; padding: 10px; border-radius: 5px;'>Solar Load Calculator | سولر لوڈ کیلکولیٹر</h3>", unsafe_allow_html=True)
st.divider()

# --- SECTION 1: APPLIANCES ---
st.subheader("1. Appliances Selection | برقی آلات کا انتخاب")
col1, col2 = st.columns(2)

with col1:
    f_p = st.number_input("Old Fans / پرانے پنکھے (100W)", min_value=0, value=0, key="fp_q")
    f_a = st.number_input("AC/DC Fans / نئے پنکھے (65W)", min_value=0, value=4, key="fa_q")
    l_o = st.number_input("Normal Bulbs / عام بلب (60W)", min_value=0, value=0, key="lo_q")
    l_l = st.number_input("LED Bulbs / ایل ای ڈی بلب (12W)", min_value=0, value=10, key="ll_q")
    m_q = st.number_input("Motor Quantity / موٹر کی تعداد", min_value=0, value=1, key="m_qty")
    m_hp = st.number_input("Motor Power / موٹر کی پاور (HP)", min_value=0.0, value=1.0, step=0.5, key="m_pwr")

with col2:
    fr_q = st.number_input("Fridge Quantity / فریج کی تعداد", min_value=0, value=1, key="fr_qty")
    fr_w = st.number_input("Fridge Watts / فریج کے واٹس", min_value=0, value=500, key="fr_pwr")
    ac_q = st.number_input("AC Quantity / اے سی کی تعداد", min_value=0, value=1, key="ac_qty")
    ac_w = st.number_input("AC Watts / اے سی کے واٹس", min_value=0, value=1500, key="ac_pwr")

st.divider()

# --- SECTION 2: MARKET RATES ---
st.subheader("2. Market Rates | مارکیٹ ریٹ")
col3, col4 = st.columns(2)

with col3:
    p_w = st.number_input("Plate Watts / پلیٹ کے واٹس", min_value=1, value=585, key="plt_w")
    p_r = st.number_input("Plate Price / پلیٹ کی قیمت (Rs)", min_value=0, value=22000, key="plt_r")
    inv_type = st.radio("Inverter Choice / انورٹر کا انتخاب", ["Hybrid Inverter (ہائبرڈ)", "Car/Simple Inverter (کار انورٹر)"], horizontal=True)
    inv_price = st.number_input("Inverter Price / انورٹر کی قیمت (Rs)", min_value=0, value=65000 if "Hybrid" in inv_type else 15000, key="inv_prc")

with col4:
    b_ah = st.number_input("Battery Ah / بیٹری کے ایمپئیر", min_value=1, value=200, key="bat_ah")
    b_r = st.number_input("Battery Price / بیٹری کی قیمت (Rs)", min_value=0, value=45000, key="bat_r")

# --- CALCULATION LOGIC ---
if st.button("Generate Technical Report | رپورٹ تیار کریں", use_container_width=True):
    # Base Loads
    normal_load_w = (f_p*100) + (f_a*65) + (l_o*60) + (l_l*12)
    heavy_load_w = (m_hp * m_q * 746) + (fr_q * fr_w) + (ac_q * ac_w)
    total_w = normal_load_w + heavy_load_w
    kw = total_w / 1000
    
    # Inverter & Battery Selection
    if kw <= 1.2: s_kw, vol, n_b, conn = 1.5, 12, 1, "Single Battery (12V)"
    elif kw <= 2.8: s_kw, vol, n_b, conn = 3, 24, 2, "1 String (2 Series - 24V)"
    elif kw <= 5.5: s_kw, vol, n_b, conn = 6, 48, 4, "1 String (4 Series - 48V)"
    else: s_kw, vol, n_b, conn = math.ceil(kw + 2), 48, 8, "2 Strings (Parallel - 48V)"
    
    n_p = math.ceil((total_w * 1.30) / p_w)
    usable_storage = (b_ah * vol * 0.8)
    
    # Backup Calculations
    backup_light = usable_storage / normal_load_w if normal_load_w > 0 else 0
    heavy_night_load = normal_load_w + (fr_q * (fr_w * 0.5)) + (ac_q * (ac_w * 0.6)) 
    backup_heavy = usable_storage / heavy_night_load if heavy_night_load > 0 else 0
    
    # Results Display
    st.markdown(f"### 📊 Total System Load | کل لوڈ: {int(total_w)}W ({kw:.2f} kW)")
    st.success(f"🏠 **Normal Load (Basic): {int(normal_load_w)} Watts**\n\n*(اے سی، فریج اور موٹر کے بغیر لوڈ)*")
    
    res1, res2 = st.columns(2)
    with res1:
        st.info(f"**Inverter ({inv_type}):**\n{s_kw}kW | Rs. {inv_price:,.0f}")
        st.success(f"**Solar Plates:**\n{n_p} Nos | Rs. {n_p * p_r:,.0f}")
    with res2:
        st.info(f"**Batteries:**\n{n_b} Nos | {conn}")
        st.success(f"**Battery Cost:**\nRs. {n_b * b_r:,.0f}")
    
    st.divider()
    st.subheader("🌙 Night Backup Estimation | رات کا بیک اپ")
    
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.warning(f"**Light Load (Fans/Bulbs Only):**\n{backup_light:.1f} Hours / گھنٹے")
    with b_col2:
        st.error(f"**Heavy Load (with AC/Fridge):**\n{backup_heavy:.1f} Hours / گھنٹے")
        
    st.divider()
    total_cost = (n_p * p_r) + (n_b * b_r) + inv_price
    st.error(f"## Grand Total / کل خرچہ: Rs. {total_cost:,.0f}")
    st.markdown("<p style='text-align: center; color: #fbbf24; font-weight: bold;'>Smart Choice for a Brighter Future!</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>Developed for NABA SOLUTIONS | PINCH BRAND © 2026</p>", unsafe_allow_html=True)
