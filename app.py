import streamlit as st
import math

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="NABA Solar Tech", page_icon="☀️", layout="centered")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1rem 0 0.5rem;'>
  <h1 style='color:#fbbf24; margin:0; font-size:2rem;'>☀️ NABA SOLAR SOLUTIONS</h1>
  <p style='color:#4ade80; font-size:1rem; margin:4px 0 0;'>Powered by NABA – Energy for Generations</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align:center; background:#1e293b; color:#fff; padding:10px; border-radius:8px;'>"
    "Solar Load Calculator &nbsp;|&nbsp; سولر لوڈ کیلکولیٹر</h3>",
    unsafe_allow_html=True
)
st.divider()

# ── SECTION 1: Appliances ────────────────────────────────────────────────────
st.subheader("1. Appliances / برقی آلات")
c1, c2 = st.columns(2)

with c1:
    fans   = st.number_input("AC/DC Fans (65W) / پنکھے",       min_value=0, value=4)
    bulbs  = st.number_input("LED Bulbs (12W) / بلب",           min_value=0, value=10)
    motor_q = st.number_input("Motor quantity / موٹر تعداد",   min_value=0, value=1)
    motor_hp = st.number_input("Motor power (HP) / موٹر پاور", min_value=0.0, value=1.0, step=0.5)

with c2:
    fridge_q = st.number_input("Fridge quantity / فریج تعداد", min_value=0, value=1)
    fridge_w = st.number_input("Fridge watts / فریج واٹس",     min_value=0, value=500)
    ac_q     = st.number_input("AC quantity / اے سی تعداد",    min_value=0, value=0)
    ac_w     = st.number_input("AC watts / اے سی واٹس",        min_value=0, value=1500)

st.divider()

# ── SECTION 2: System & Rates ────────────────────────────────────────────────
st.subheader("2. System & Rates / سسٹم اور ریٹ")
c3, c4 = st.columns(2)

with c3:
    panel_w     = st.number_input("Panel wattage / پینل واٹ",       min_value=1,  value=585)
    panel_price = st.number_input("Panel price (Rs) / پینل قیمت",   min_value=0,  value=21000)
    bat_ah      = st.number_input("Battery Ah / بیٹری اے ایچ",      min_value=1,  value=200)
    bat_price   = st.number_input("Battery price (Rs) / بیٹری قیمت",min_value=0,  value=45000)

with c4:
    inv_type = st.radio(
        "Inverter type / انورٹر قسم",
        ["Hybrid Inverter", "Car / Simple Inverter"],
        horizontal=True
    )
    is_hybrid = "Hybrid" in inv_type

    # Sensible default price based on inverter type
    default_inv_price = 65000 if is_hybrid else 12000
    inv_price = st.number_input(
        "Inverter price (Rs) / انورٹر قیمت",
        min_value=0,
        value=default_inv_price
    )

    sys_vol = st.selectbox(
        "Battery system voltage / بیٹری وولٹیج",
        ["Auto Select", "12V (1 Battery)", "24V (2 Batteries)", "48V (4 Batteries)"]
    )

# ── SECTION 3: Charger (simple inverter only) ────────────────────────────────
ctrl_price = 0
ctrl_name  = ""
conn_type  = "Parallel"   # safe default — always defined

if not is_hybrid:
    st.divider()
    st.subheader("3. Charger & Connection / چارجر اور کنیکشن")
    cx1, cx2 = st.columns(2)

    with cx1:
        conn_type   = st.radio("Solar connection", ["Parallel (High Amps)", "Series (High Volts)"])
        ctrl_choice = st.selectbox("Charger type", ["PWM (BMW)", "MPPT"])

    with cx2:
        ctrl_amp    = st.selectbox("Charger amps", ["30A", "40A", "60A", "80A", "100A", "120A"])
        default_ctrl_price = 8500 if "PWM" in ctrl_choice else 16500
        ctrl_price  = st.number_input(
            f"Price for {ctrl_amp} {ctrl_choice} (Rs)",
            min_value=0,
            value=default_ctrl_price
        )
        ctrl_name = f"{ctrl_choice} {ctrl_amp}"

st.divider()

# ── CALCULATE ────────────────────────────────────────────────────────────────
if st.button("⚡ Generate Final Report / رپورٹ بنائیں", use_container_width=True, type="primary"):

    # Load calculations
    fan_load    = fans    * 65
    bulb_load   = bulbs   * 12
    motor_load  = motor_q * motor_hp * 746
    fridge_load = fridge_q * fridge_w
    ac_load     = ac_q    * ac_w
    total_w     = fan_load + bulb_load + motor_load + fridge_load + ac_load

    if total_w == 0:
        st.error("⚠️ Please enter at least one appliance load.")
        st.stop()

    kw = total_w / 1000

    # Voltage selection
    if sys_vol == "Auto Select":
        vol = 12 if kw <= 1.2 else (24 if kw <= 2.8 else 48)
    else:
        vol = int(sys_vol.split("V")[0])

    n_bat   = vol // 12
    n_panel = math.ceil((total_w * 1.30) / panel_w)

    # Charger amps recommendation (simple inverter)
    plate_amps = 11.5
    if not is_hybrid:
        if "Parallel" in conn_type:
            required_amps = math.ceil(n_panel * plate_amps * 1.2)
        else:
            required_amps = math.ceil(plate_amps * 1.2)  # series: current stays same
    else:
        required_amps = 0

    # Night backup (fans + bulbs only — motors/AC are not usually run at night)
    normal_load = fan_load + bulb_load
    backup_load = normal_load if normal_load > 0 else total_w
    usable_wh   = bat_ah * vol * 0.8
    backup_h    = usable_wh / backup_load

    # Cost totals
    panel_cost = n_panel * panel_price
    bat_cost   = n_bat   * bat_price
    grand_total = panel_cost + bat_cost + inv_price + ctrl_price

    # ── Display ──────────────────────────────────────────────────────────────
    st.markdown(f"### 📊 System Estimate: {int(total_w):,}W &nbsp;({kw:.2f} kW)")

    # Load breakdown
    with st.expander("Load breakdown / لوڈ تفصیل", expanded=True):
        lb1, lb2 = st.columns(2)
        rows = [
            ("Fans", fan_load),
            ("Bulbs", bulb_load),
            ("Motor(s)", motor_load),
            ("Fridge(s)", fridge_load),
            ("AC unit(s)", ac_load),
        ]
        for i, (name, w) in enumerate(rows):
            if w > 0:
                col = lb1 if i % 2 == 0 else lb2
                col.metric(name, f"{int(w):,} W")

    # Voltage / panel / battery summary
    m1, m2, m3 = st.columns(3)
    m1.metric("Battery system", f"{vol}V ({n_bat} unit{'s' if n_bat > 1 else ''})")
    m2.metric("Solar panels", f"{n_panel} × {panel_w}W")
    m3.metric("Night backup*", f"~{backup_h:.1f} hr")

    if not is_hybrid:
        st.info(
            f"⚙️ **{conn_type}** — recommended minimum charger size: **{required_amps}A**  "
            f"(selected: {ctrl_name})"
        )

    st.divider()

    # Cost breakdown
    st.subheader("Cost Breakdown / لاگت کی تفصیل")
    r1, r2 = st.columns(2)

    with r1:
        st.info(f"**Solar panels** ({n_panel} nos)\n\nRs. {panel_cost:,.0f}")
        st.info(f"**Inverter**\n\nRs. {inv_price:,.0f}")

    with r2:
        st.info(f"**Batteries** ({n_bat} nos)\n\nRs. {bat_cost:,.0f}")
        if ctrl_price > 0:
            st.info(f"**{ctrl_name}**\n\nRs. {ctrl_price:,.0f}")

    st.markdown(
        f"<div style='background:#1e293b;color:#fbbf24;text-align:center;"
        f"padding:18px;border-radius:10px;font-size:1.4rem;font-weight:bold;margin-top:1rem;'>"
        f"Grand Total / کل لاگت &nbsp;=&nbsp; Rs. {grand_total:,.0f}</div>",
        unsafe_allow_html=True
    )

    st.caption(
        "\\* Night backup uses fans + bulbs only (motors and AC are excluded as they run intermittently). "
        "Panel count includes a 30% safety margin. Installation, wiring, and labour are not included."
    )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    "<p style='text-align:center;color:gray;font-size:11px;margin-top:2rem;'>"
    "NABA SOLUTIONS | PINCH BRAND © 2026</p>",
    unsafe_allow_html=True
)
