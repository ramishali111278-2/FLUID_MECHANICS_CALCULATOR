import streamlit as st
import math

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pipe Flow & Pressure Drop Calculator",
    page_icon="💧",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .block-container { padding-top: 2rem; }
    .result-box {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.4rem 0;
        font-size: 1.05rem;
    }
    .regime-laminar     { background: linear-gradient(135deg, #2e7d32, #1b5e20); }
    .regime-transitional{ background: linear-gradient(135deg, #f57f17, #e65100); }
    .regime-turbulent   { background: linear-gradient(135deg, #c62828, #b71c1c); }
    h1 { color: #0d47a1; }
    .footer { text-align:center; color:#aaa; font-size:0.8rem; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("# 💧 Pipe Flow & Pressure Drop Calculator")
st.caption("Group 10 - ICT Project")
st.markdown("---")

# ── Input Parameters ──────────────────────────────────────────────────────────
st.subheader("📥 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    pipe_length = st.number_input(
        "Pipe Length (m)",
        min_value=0.01, max_value=10000.0,
        value=10.0, step=1.0, format="%.2f"
    )
    fluid_velocity = st.number_input(
        "Fluid Velocity (m/s)",
        min_value=0.001, max_value=1000.0,
        value=1.5, step=0.1, format="%.2f"
    )
    friction_factor = st.number_input(
        "Friction Factor (f)  [Darcy-Weisbach]",
        min_value=0.001, max_value=1.0,
        value=0.02, step=0.001, format="%.4f"
    )

with col2:
    pipe_diameter = st.number_input(
        "Pipe Diameter (m)",
        min_value=0.001, max_value=100.0,
        value=0.10, step=0.01, format="%.3f"
    )
    fluid_density = st.number_input(
        "Fluid Density (kg/m³)",
        min_value=0.1, max_value=20000.0,
        value=1000.0, step=10.0, format="%.2f"
    )
    dynamic_viscosity = st.number_input(
        "Dynamic Viscosity (Pa·s)",
        min_value=0.000001, max_value=100.0,
        value=0.001, step=0.0001, format="%.6f"
    )

st.markdown("---")

# ── Calculate ─────────────────────────────────────────────────────────────────
if st.button("⚡ Calculate", use_container_width=True, type="primary"):

    Re = (fluid_density * fluid_velocity * pipe_diameter) / dynamic_viscosity

    if Re < 2300:
        regime = "Laminar"
        regime_class = "regime-laminar"
        regime_emoji = "🟢"
    elif Re < 4000:
        regime = "Transitional"
        regime_class = "regime-transitional"
        regime_emoji = "🟡"
    else:
        regime = "Turbulent"
        regime_class = "regime-turbulent"
        regime_emoji = "🔴"

    delta_P = friction_factor * (pipe_length / pipe_diameter) * 0.5 * fluid_density * fluid_velocity ** 2

    area = math.pi * (pipe_diameter / 2) ** 2
    flow_rate_m3s = area * fluid_velocity
    flow_rate_Ls  = flow_rate_m3s * 1000

    velocity_head = (fluid_velocity ** 2) / (2 * 9.81)
    mass_flow = fluid_density * flow_rate_m3s

    st.subheader("📊 Results")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f'<div class="result-box"><b>Reynolds Number (Re)</b><br>{Re:,.1f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><b>Pressure Drop (ΔP)</b><br>{delta_P:,.4f} Pa<br>{delta_P/1000:,.6f} kPa</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><b>Velocity Head</b><br>{velocity_head:.4f} m</div>', unsafe_allow_html=True)

    with c2:
        st.markdown(f'<div class="result-box {regime_class}"><b>Flow Regime</b><br>{regime_emoji} {regime}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><b>Volumetric Flow Rate (Q)</b><br>{flow_rate_m3s:.6f} m³/s<br>{flow_rate_Ls:.4f} L/s</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><b>Mass Flow Rate (ṁ)</b><br>{mass_flow:.4f} kg/s</div>', unsafe_allow_html=True)

    with st.expander("📐 Formulas Used"):
        st.latex(r"Re = \frac{\rho V D}{\mu}")
        st.latex(r"\Delta P = f \cdot \frac{L}{D} \cdot \frac{1}{2} \rho V^2")
        st.latex(r"Q = A \cdot V = \frac{\pi D^2}{4} \cdot V")

st.markdown('<div class="footer">Group 10 · ICT Project · Fluid Mechanics Calculator</div>', unsafe_allow_html=True)
