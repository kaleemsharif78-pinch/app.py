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
    f_p = st.number_input("Old Fans / پرانے پنکھے (100W)", min_value=0, value=0)
    f_a = st.number_input("AC/DC Fans / نئے پنکھے (65W)", min_value=0, value=4)
    l_l = st.number_input("LED Bulbs / ایل ای ڈی بلب (12W)", min_value=0, value=10)
    m_q = st.number_input("Motor Quantity / موٹر کی تعداد", min_value=0, value=1)
    m_hp = st.number_input("Motor Power / موٹر کی پاور (HP)", min_value=0.0, value=1.0, step=0.5)

with col2:
    fr_q = st.number_input("Fridge Quantity / فریج کی تعداد", min_value=0, value=1)
    fr_w = st.number_input("Fridge Watts / فریج کے واٹس", min_value=0, value=500)
    ac_q = st.number_input("AC Quantity / اے سی کی تعداد", min_value=0, value=0)
    ac_w = st.number_input("AC Watts / اے سی کے واٹس", min_value=0, value=1500)

st.divider()

# --- SECTION 2: SYSTEM & RATES ---
st.subheader("2. System & Rates | سسٹم اور ریٹ")
col3, col4 = st.columns(2)

with col3:
    p_w = st.number_input("Plate Watts / پلیٹ کے واٹس", min_value=1, value=585)
    p_r = st.number_input("Plate Price / پلیٹ کی قیمت (Rs)", min_value=0, value=21000)
    inv_type = st.radio("Inverter Type / انورٹر کی قسم", ["Hybrid Inverter", "Car/Simple Inverter"], horizontal=True)
    inv_price = st.number_input("Inverter Price / انورٹر کی قیمت (Rs)", min_value=0, value=65000 if "Hybrid" in inv_type else 12000)

with col4:
    b_ah = st.number_input("Battery Ah / بیٹری کے ایمپئیر", min_value=1, value=200)
    b_r = st.number_input("Battery Price / بیٹری کی قیمت (Rs)", min_value=0, value=45000)
    sys_vol_choice = st.selectbox("Battery System / بیٹری سسٹم", ["Auto Select", "12V (1 Battery)", "24V (2 Batteries)", "48V (4 Batteries)"])

# --- CHARGER CONTROLLER (Admin Control for Simple Inverters) ---
ctrl_price = 0
ctrl_name = ""
if "Car" in inv_type:
    st.markdown("---")
    st.info("ℹ️ Simple Inverter ke liye Charger Controller lazmi hai")
    ctrl_choice = st.selectbox("Select Charger / چارجر منتخب کریں", ["PWM Charger (BMW Style)", "MPPT Charger (Best Performance)"])
    if "PWM" in ctrl_choice:
        ctrl_price = st.number_input("PWM Price / قیمت", value=6500)
        ctrl_name = "PWM Charger"
    else:
        ctrl_price = st.number_input("MPPT Price / قیمت", value=14500)
        ctrl_name = "MPPT Charger"

# --- CALCULATION ---
if st.button("Generate Final Report | رپورٹ تیار کریں", use_container_width=True):
    normal_load = (f_p*100) + (f_a*65) + (l_l*12)
    heavy_load = (m_hp * m_q * 746) + (fr_q * fr_w) + (ac_q * ac_w)
    total_w = normal_load + heavy_load
    kw = total_w / 1000
    
    # Volts logic
    if sys_vol_choice == "Auto Select":
        vol = 12 if kw <= 1.2 else (24 if kw <= 2.8 else 48)
    else:
        vol = int(sys_vol_choice.split('V')[0])
    
    n_b = vol // 12
    n_p = math.ceil((total_w * 1.30) / p_w)
    usable_storage = (b_ah * vol * 0.8)
    
    # Backup estimation
    backup_light = usable_storage / normal_load if normal_load > 0 else 0
    heavy_night = normal_load + (fr_q * (fr_w * 0.5)) + (ac_q * (ac_w * 0.6))
    backup_heavy = usable_storage / heavy_night if heavy_night > 0 else 0
    
    # Display Results
    st.markdown(f"### 📊 Total Load Assessment: {int(total_w)}W ({kw:.2f} kW)")
    st.success(f"🏠 **Normal Load (Basic): {int(normal_load)} Watts**")
    
    r1, r2 = st.columns(2)
    with r1:
        st.info(f"**Inverter:** Rs. {inv_price:,.0f}")
        if ctrl_price > 0:
            st.warning(f"**{ctrl_name}:** Rs. {ctrl_price:,.0f}")
        st.success(f"**Plates ({n_p} Nos):** Rs. {n_p * p_r:,.0f}")
    with r2:
        st.info(f"**Batteries ({n_b} Nos):** Rs. {n_b * b_r:,.0f}")
        st.warning(f"**Backup (Fans/Lights):** {backup_light:.1f} Hr")
        st.error(f"**Backup (Full Load):** {backup_heavy:.1f} Hr")
    
    st.divider()
    grand_total = (n_p * p_r) + (n_b * b_r) + inv_price + ctrl_price
    st.error(f"## Grand Total / کل خرچہ: Rs. {grand_total:,.0f}")
    st.markdown("<p style='text-align: center; color: #fbbf24; font-weight: bold;'>Smart Choice with NABA SOLAR SOLUTIONS</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>NABA SOLUTIONS | PINCH BRAND © 2026</p>", unsafe_allow_html=True)
