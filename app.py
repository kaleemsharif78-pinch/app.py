import streamlit as st
import math

# Page Configuration
st.set_page_config(page_title="NABA Solar Tech", page_icon="☀️")

# Branding Header
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>NABA SOLAR SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #94a3b8;'>Solar Load Calculator | سولر لوڈ کیلکولیٹر</h3>", unsafe_allow_html=True)
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

# --- SECTION 2: RATES & SPECS ---
st.subheader("2. Market Rates | مارکیٹ ریٹ")
col3, col4 = st.columns(2)

with col3:
    p_w = st.number_input("Plate Watts / پلیٹ کے واٹس", min_value=1, value=585, key="plt_w")
    p_r = st.number_input("Plate Price / پلیٹ کی قیمت (Rs)", min_value=0, value=22000, key="plt_r")
    inv_type = st.selectbox("Inverter Type / انورٹر کی قسم", ["Hybrid Inverter", "Off-Grid System"])

with col4:
    b_ah = st.number_input("Battery Ah / بیٹری کے ایمپئیر", min_value=1, value=200, key="bat_ah")
    b_r = st.number_input("Battery Price / بیٹری کی قیمت (Rs)", min_value=0, value=45000, key="bat_r")

# --- CALCULATION LOGIC ---
if st.button("Generate Report | رپورٹ تیار کریں", use_container_width=True):
    # Base Loads
    motor_load = (m_hp * m_q * 746)
    fridge_load = (fr_q * fr_w)
    ac_load = (ac_q * ac_w)
    fans_bulbs_load = (f_p*100) + (f_a*65) + (l_o*60) + (l_l*12)
    
    total_w = fans_bulbs_load + fridge_load + ac_load + motor_load
    kw = total_w / 1000
    
    # Inverter Logic
    if kw <= 1.2:
        s_kw, vol, n_b, conn = 1.5, 12, 1, "Single Battery (12V)"
    elif kw <= 2.8:
        s_kw, vol, n_b, conn = 3, 24, 2, "1 String (2 Series - 24V)"
    elif kw <= 5.5:
        s_kw, vol, n_b, conn = 6, 48, 4, "1 String (4 Series - 48V)"
    else:
        s_kw, vol, n_b, conn = math.ceil(kw + 2), 48, 8, "2 Strings (Parallel - 48V)"
    
    n_p = math.ceil((total_w * 1.30) / p_w)
    
    # Backup Logic
    usable_storage = (b_ah * vol * 0.8) # 80% Depth of discharge
    
    # Option 1: Light Load (Only Fans/Bulbs)
    backup_light = usable_storage / fans_bulbs_load if fans_bulbs_load > 0 else 0
    
    # Option 2: Heavy Load (Fans + Fridge + AC) - Motor typically excluded at night
    heavy_night_load = fans_bulbs_load + (fr_q * (fr_w * 0.5)) + (ac_q * (ac_w * 0.6)) 
    backup_heavy = usable_storage / heavy_night_load if heavy_night_load > 0 else 0
    
    # Results Display
    st.markdown(f"### 📊 Total Load | کل لوڈ: {int(total_w)}W ({kw:.2f} kW)")
    
    r1, r2 = st.columns(2)
    with r1:
        st.info(f"**Inverter / انورٹر:**\n{s_kw}kW ({vol}V)")
        st.success(f"**Solar Plates / پلیٹیں:**\n{n_p} Nos | Rs. {n_p * p_r:,.0f}")
    
    with r2:
        st.info(f"**Batteries / بیٹریاں:**\n{n_b} Nos | {conn}")
        st.success(f"**Battery Cost / قیمت:**\nRs. {n_b * b_r:,.0f}")
    
    st.divider()
    st.subheader("🌙 Night Backup Estimation | رات کا بیک اپ")
    
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.warning(f"**Light Load (Fans/Bulbs Only):**\n{backup_light:.1f} Hours / گھنٹے\n*(بغیر فریج اور اے سی کے)*")
    with b_col2:
        st.error(f"**Heavy Load (with AC/Fridge):**\n{backup_heavy:.1f} Hours / گھنٹے\n*(فریج اور اے سی کے ساتھ)*")
        
    st.divider()
    st.error(f"## Grand Total / کل خرچہ: Rs. {(n_p * p_r) + (n_b * b_r):,.0f}")

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>NABA SOLUTIONS | PINCH BRAND © 2026</p>", unsafe_allow_html=True)
