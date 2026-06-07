import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

st.set_page_config(page_title="Pipe Flow Calculator", page_icon="💧", layout="centered")

st.markdown("""
<style>
    body { background-color: #0a0e1a; }
    .main { background-color: #0a0e1a; }
    .block-container { padding-top: 1.5rem; }
    .title {
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        color: #00c8ff;
        letter-spacing: 2px;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    .result-card {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: white;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        margin: 0.3rem 0;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(0,150,255,0.2);
    }
    .green  { background: linear-gradient(135deg, #2e7d32, #1b5e20) !important; }
    .orange { background: linear-gradient(135deg, #e65100, #bf360c) !important; }
    .red    { background: linear-gradient(135deg, #b71c1c, #880e0e) !important; }
    .footer { text-align:center; color:#555; font-size:0.75rem; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💧 Pipe Flow Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Group 10 — ICT Project — Fluid Mechanics</div>', unsafe_allow_html=True)

st.markdown("### ⚙️ Enter Values")
c1, c2 = st.columns(2)
with c1:
    L   = st.number_input("📏 Pipe Length (m)",       min_value=0.01, value=10.0,   step=1.0)
    V   = st.number_input("💨 Fluid Velocity (m/s)",  min_value=0.01, value=1.5,    step=0.1)
    f   = st.number_input("🔧 Friction Factor (f)",   min_value=0.001,value=0.02,   step=0.001, format="%.3f")
with c2:
    D   = st.number_input("⭕ Pipe Diameter (m)",      min_value=0.001,value=0.10,   step=0.01,  format="%.3f")
    rho = st.number_input("🧪 Fluid Density (kg/m³)", min_value=0.1,  value=1000.0, step=10.0)
    mu  = st.number_input("🌊 Viscosity (Pa·s)",       min_value=1e-6, value=0.001,  step=0.0001,format="%.4f")

st.markdown("---")

if st.button("⚡ CALCULATE", use_container_width=True, type="primary"):

    Re      = (rho * V * D) / mu
    delta_P = f * (L / D) * 0.5 * rho * V**2
    Q       = math.pi * (D/2)**2 * V
    m_dot   = rho * Q

    regime = "Laminar"      if Re < 2300 else "Transitional" if Re < 4000 else "Turbulent"
    color  = "green"        if Re < 2300 else "orange"       if Re < 4000 else "red"
    emoji  = "🟢"           if Re < 2300 else "🟡"           if Re < 4000 else "🔴"

    st.markdown("### 📊 Results")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f'<div class="result-card {color}"><b>{emoji} Flow Regime</b><br>{regime}<br><small>Re = {Re:,.0f}</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><b>🔴 Pressure Drop</b><br>{delta_P:,.2f} Pa<br><small>{delta_P/1000:.4f} kPa</small></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="result-card"><b>💧 Flow Rate</b><br>{Q:.5f} m³/s<br><small>{Q*1000:.3f} L/s</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><b>⚖️ Mass Flow Rate</b><br>{m_dot:.3f} kg/s</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Graphs")

    plt.style.use('dark_background')
    vel_range = np.linspace(0.1, max(V * 2, 5), 200)
    Re_range  = (rho * vel_range * D) / mu
    dP_range  = f * (L / D) * 0.5 * rho * vel_range**2
    len_range = np.linspace(1, max(L * 2, 20), 200)
    dP_len    = f * (len_range / D) * 0.5 * rho * V**2

    # Graph 1 — Pressure Drop vs Velocity
    fig1, ax1 = plt.subplots(figsize=(7, 3.5))
    ax1.plot(vel_range, dP_range, color='#00c8ff', linewidth=2.5)
    ax1.axvline(V, color='#ff4444', linestyle='--', linewidth=1.5, label=f'V = {V} m/s')
    ax1.scatter([V], [delta_P], color='#ff4444', s=100, zorder=5)
    ax1.fill_between(vel_range, dP_range, alpha=0.1, color='#00c8ff')
    ax1.set_xlabel('Velocity (m/s)', color='#aaa')
    ax1.set_ylabel('Pressure Drop (Pa)', color='#aaa')
    ax1.set_title('Pressure Drop vs Velocity', color='white', fontweight='bold')
    ax1.legend(); ax1.grid(alpha=0.15)
    ax1.set_facecolor('#0d1117')
    fig1.patch.set_facecolor('#0d1117')
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # Graph 2 — Reynolds Number vs Velocity
    fig2, ax2 = plt.subplots(figsize=(7, 3.5))
    ax2.fill_between(vel_range, 0, 2300,                    alpha=0.2, color='#00e676', label='Laminar')
    ax2.fill_between(vel_range, 2300, 4000,                 alpha=0.2, color='#ffab00', label='Transitional')
    ax2.fill_between(vel_range, 4000, max(Re_range)*1.05,   alpha=0.15,color='#ff1744', label='Turbulent')
    ax2.plot(vel_range, Re_range, color='#00c8ff', linewidth=2.5)
    ax2.axvline(V, color='#ff4444', linestyle='--', linewidth=1.5, label=f'V = {V} m/s')
    ax2.scatter([V], [Re], color='#ff4444', s=100, zorder=5)
    ax2.set_xlabel('Velocity (m/s)', color='#aaa')
    ax2.set_ylabel('Reynolds Number', color='#aaa')
    ax2.set_title('Reynolds Number vs Velocity', color='white', fontweight='bold')
    ax2.legend(loc='upper left'); ax2.grid(alpha=0.15)
    ax2.set_facecolor('#0d1117')
    fig2.patch.set_facecolor('#0d1117')
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # Graph 3 — Pressure Drop vs Pipe Length
    fig3, ax3 = plt.subplots(figsize=(7, 3.5))
    ax3.plot(len_range, dP_len, color='#ce93d8', linewidth=2.5)
    ax3.axvline(L, color='#ff4444', linestyle='--', linewidth=1.5, label=f'L = {L} m')
    ax3.scatter([L], [delta_P], color='#ff4444', s=100, zorder=5)
    ax3.fill_between(len_range, dP_len, alpha=0.1, color='#ce93d8')
    ax3.set_xlabel('Pipe Length (m)', color='#aaa')
    ax3.set_ylabel('Pressure Drop (Pa)', color='#aaa')
    ax3.set_title('Pressure Drop vs Pipe Length', color='white', fontweight='bold')
    ax3.legend(); ax3.grid(alpha=0.15)
    ax3.set_facecolor('#0d1117')
    fig3.patch.set_facecolor('#0d1117')
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    with st.expander("📐 Formulas"):
        st.latex(r"Re = \frac{\rho V D}{\mu}")
        st.latex(r"\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho V^2}{2}")
        st.latex(r"Q = \frac{\pi D^2}{4} \cdot V")

st.markdown('<div class="footer">Group 10 · ICT Project · Fluid Mechanics</div>', unsafe_allow_html=True)
