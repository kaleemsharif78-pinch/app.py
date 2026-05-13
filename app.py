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
    f_a = st.number_input("AC/DC Fans / نئے پنکھے (65W)", min_value=0, value=4)
    l_l = st.number_input("LED Bulbs / ایل ای ڈی بلب (12W)", min_value=0, value=10)
    m_q = st.number_input("Motor Quantity / موٹر کی تعداد", min_value=0, value=1) # واپس شامل کر دی
    m_hp = st.number_input("Motor Power / موٹر پاور (HP)", min_value=0.0, value=1.0, step=0.5)

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
    p_w = st.number_input("Plate Watts", min_value=1, value=585)
    p_r = st.number_input("Plate Price (Rs)", min_value=0, value=21000)
    inv_type = st.radio("Inverter Choice", ["Hybrid Inverter", "Car/Simple Inverter"], horizontal=True)
    inv_price = st.number_input("Inverter Price (Rs)", min_value=0, value=65000 if "Hybrid" in inv_type else 12000)

with col4:
    b_ah = st.number_input("Battery Ah", min_value=1, value=200)
    b_r = st.number_input("Battery Price (Rs)", min_value=0, value=45000)
    sys_vol = st.selectbox("Battery System", ["Auto Select", "12V (1 Battery)", "24V (2 Batteries)", "48V (4 Batteries)"])

# --- CHARGER & CONNECTION LOGIC ---
ctrl_price = 0
ctrl_name = ""
if "Car" in inv_type:
    st.markdown("---")
    st.info("ℹ️ Charger & Connection Settings")
    cx1, cx2 = st.columns(2)
    with cx1:
        conn_type = st.radio("Solar Connection", ["Parallel (High Amps)", "Series (High Volts)"])
    with cx2:
        ctrl_choice = st.selectbox("Charger Type", ["PWM (BMW)", "MPPT"])
        amp_select = st.selectbox("Charger Amps", ["30A", "40A", "60A", "80A", "100A", "120A"])
    
    ctrl_price = st.number_input(f"Enter Price for {amp_select} {ctrl_choice}", value=8500 if "PWM" in ctrl_choice else 16500)
    ctrl_name = f"{ctrl_choice} {amp_select}"

# --- CALCULATION ---
if st.button("Generate Final Report", use_container_width=True):
    # Total Load Calculation including multiple motors
    normal_load = (f_a*65) + (l_l*12)
    motor_load = (m_hp * m_q * 746) 
    fridge_load = (fr_q * fr_w)
    ac_load = (ac_q * ac_w)
    
    total_w = normal_load + motor_load + fridge_load + ac_load
    kw = total_w / 1000
    
    # Voltage logic
    if sys_vol == "Auto Select":
        vol = 12 if kw <= 1.2 else (24 if kw <= 2.8 else 48)
    else:
        vol = int(sys_vol.split('V')[0])
    
    n_b = vol // 12
    n_p = math.ceil((total_w * 1.30) / p_w)
    
    # Amps Logic for Display
    plate_amps = 11.5 # Standard for high watts plates
    if conn_type == "Parallel (High Amps)":
        required_amps = n_p * plate_amps
    else:
        required_amps = plate_amps # In series, amps remain same as one plate
    
    # Backup
    usable_storage = (b_ah * vol * 0.8)
    backup_h = usable_storage / normal_load if normal_load > 0 else 0
    
    # Result Display
    st.markdown(f"### 📊 Final Assessment: {int(total_w)}W ({kw:.2f} kW)")
    
    if "Car" in inv_type:
        st.warning(f"⚙️ **{conn_type}:** Required Controller Amps: **{math.ceil(required_amps * 1.2)}A**")

    r1, r2 = st.columns(2)
    with r1:
        st.info(f"**Inverter:** Rs. {inv_price:,.0f}")
        if ctrl_price > 0:
            st.warning(f"**{ctrl_name}:** Rs. {ctrl_price:,.0f}")
        st.success(f"**Solar Plates ({n_p} Nos):** Rs. {n_p * p_r:,.0f}")
    with r2:
        st.info(f"**Batteries ({n_b} Nos):** Rs. {n_b * b_r:,.0f}")
        st.warning(f"**Night Backup:** ~{backup_h:.1f} Hr")
    
    st.divider()
    grand_total = (n_p * p_r) + (n_b * b_r) + inv_price + ctrl_price
    st.error(f"## Grand Total: Rs. {grand_total:,.0f}")

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>NABA SOLUTIONS | PINCH BRAND © 2026</p>", unsafe_allow_html=True)
