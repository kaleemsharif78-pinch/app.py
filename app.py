import streamlit as st
import math

st.set_page_config(page_title="NABA Solar Web", page_icon="☀️")
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>NABA SOLAR SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>WEB VERSION FOR MOBILE</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    f_p = st.number_input("Old Fans (100W)", 0)
    f_a = st.number_input("AC/DC Fans (65W)", 0, value=4)
    l_o = st.number_input("Normal Bulbs (60W)", 0)
    l_l = st.number_input("LED Bulbs (12W)", 0, value=10)
    fr_q = st.number_input("Fridge Qty", 0, value=1)
    fr_w = st.number_input("Fridge Watts", 0, value=500)
with col2:
    ac_q = st.number_input("AC Qty", 0, value=1)
    ac_w = st.number_input("AC Watts", 0, value=1500)
    m_hp = st.number_input("Motor HP", 0.0, value=1.0)
    b_ah = st.number_input("Battery Ah", 0, value=200)
    b_r = st.number_input("Battery Price", 0)
    p_w = st.number_input("Plate Watts", 0, value=585)
    p_r = st.number_input("Plate Price", 0)

if st.button("GENERATE WEB REPORT"):
    total_w = (f_p*100) + (f_a*65) + (l_o*60) + (l_l*12) + (fr_q*fr_w) + (ac_q*ac_w) + (m_hp*746)
    kw = total_w / 1000
    n_p = math.ceil((total_w * 1.30) / p_w)
    s_kw = math.ceil(kw + 1.5)
    vol = 24 if s_kw <= 3 else 48
    n_b = 2 if s_kw <= 3 else (4 if s_kw <= 6 else 8)
    night_load = (f_p*100) + (f_a*65) + (l_o*60) + (l_l*12) + (fr_q*fr_w)
    hours = (b_ah * vol * 0.8) / night_load if night_load > 0 else 0
    
    st.success(f"LOAD: {int(total_w)}W | INVERTER: {s_kw}kW")
    st.info(f"PLATES: {n_p} Nos | Cost: Rs. {n_p*p_r:,.0f}")
    st.info(f"BATTERIES: {n_b} Nos | Cost: Rs. {n_b*b_r:,.0f}")
    st.warning(f"BACKUP: {hours:.1f} Hours")
    st.error(f"TOTAL: Rs. {(n_p*p_r) + (n_b*b_r):,.0f}")
    # --- اس حصے کو اپنے app.py میں اپ ڈیٹ کریں ---
col1, col2 = st.columns(2)
with col1:
    f_p = st.number_input("Old Fans (100W)", 0, value=0) # یہاں 0 کر دیا
    f_a = st.number_input("AC/DC Fans (65W)", 0, value=0) # یہاں 0 کر دیا
    l_o = st.number_input("Normal Bulbs (60W)", 0, value=0)
    l_l = st.number_input("LED Bulbs (12W)", 0, value=0) # یہاں 0 کر دیا
    fr_q = st.number_input("Fridge Qty", 0, value=0) # یہاں 0 کر دیا
    fr_w = st.number_input("Fridge Watts", 0, value=500)
with col2:
    ac_q = st.number_input("AC Qty", 0, value=0)
    ac_w = st.number_input("AC Watts", 0, value=1500)
    m_hp = st.number_input("Motor HP", 0.0, value=0.0) # موٹر بھی زیرو
    b_ah = st.number_input("Battery Ah", 0, value=0)
    b_r = st.number_input("Battery Price", 0, value=0)
    p_w = st.number_input("Plate Watts", 0, value=585)
    p_r = st.number_input("Plate Price", 0, value=0)
