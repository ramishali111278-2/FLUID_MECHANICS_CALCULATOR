import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import matplotlib
matplotlib.use('Agg')

st.set_page_config(page_title="Pipe Flow & Pressure Drop Calculator", page_icon="💧", layout="wide")

st.markdown("""
<style>
    .main { background-color: #1a1a2e; }
    .block-container { padding-top: 1rem; }
    .big-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00e5ff;
        letter-spacing: 4px;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 20px #00e5ff;
        padding: 1rem;
        border: 2px solid #00e5ff;
        border-radius: 8px;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #0d0d2b, #1a1a3e);
    }
    .section-title {
        background: linear-gradient(90deg, #003366, #0055aa);
        color: white;
        padding: 0.4rem 1rem;
        font-weight: bold;
        font-size: 0.95rem;
        border-left: 4px solid #00e5ff;
        margin-bottom: 0.8rem;
    }
    .result-card {
        background: linear-gradient(135deg, #003366, #001a4d);
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #00e5ff;
        font-size: 0.95rem;
    }
    .green  { border-left: 4px solid #00e676 !important; background: linear-gradient(135deg, #003300, #001a00) !important; }
    .orange { border-left: 4px solid #ffab00 !important; background: linear-gradient(135deg, #332200, #1a1100) !important; }
    .red    { border-left: 4px solid #ff1744 !important; background: linear-gradient(135deg, #330000, #1a0000) !important; }
    .stNumberInput label { color: #00e5ff !important; font-size: 0.85rem !important; }
    .stButton button {
        background: linear-gradient(135deg, #003399, #0055cc) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        border: 2px solid #00e5ff !important;
        border-radius: 6px !important;
    }
    .footer { text-align:center; color:#444; font-size:0.75rem; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">💧 PIPE FLOW & PRESSURE DROP CALCULATOR</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; background:linear-gradient(135deg,#0d1b2a,#1a2a3a);
border:1px solid #00e5ff; border-radius:10px; padding:0.8rem; margin-bottom:1rem;">
    <span style="color:#aaa; font-size:0.8rem; letter-spacing:2px;">GROUP 10 — ICT PROJECT — FLUID MECHANICS</span><br><br>
    <span style="color:#00e5ff; font-size:1rem; font-weight:bold;">👤 Ahmed Rashid</span>
    <span style="color:#555;"> | </span>
    <span style="color:#aaa; font-size:0.85rem;">25-ME-15</span>
    &nbsp;&nbsp;&nbsp;
    <span style="color:#00e5ff; font-size:1rem; font-weight:bold;">👤 Sheharyar Naveed</span>
    <span style="color:#555;"> | </span>
    <span style="color:#aaa; font-size:0.85rem;">25-ME-35</span>
    &nbsp;&nbsp;&nbsp;
    <span style="color:#00e5ff; font-size:1rem; font-weight:bold;">👤 Ramish Ali</span>
    <span style="color:#555;"> | </span>
    <span style="color:#aaa; font-size:0.85rem;">25-ME-87</span>
</div>
""", unsafe_allow_html=True)

# ── Layout: Left inputs | Right diagram ──────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="section-title">⚙️ INPUT PARAMETERS</div>', unsafe_allow_html=True)
    L   = st.number_input("📏 Pipe Length (m)",        min_value=0.01, value=10.0,   step=1.0)
    D   = st.number_input("⭕ Pipe Diameter (m)",       min_value=0.001,value=0.10,   step=0.01,  format="%.3f")
    V   = st.number_input("💨 Fluid Velocity (m/s)",   min_value=0.01, value=1.5,    step=0.1)
    rho = st.number_input("🧪 Fluid Density (kg/m³)",  min_value=0.1,  value=1000.0, step=10.0)
    f   = st.number_input("🔧 Friction Factor (f)",    min_value=0.001,value=0.02,   step=0.001, format="%.3f")
    mu  = st.number_input("🌊 Viscosity (Pa·s)",        min_value=1e-6, value=0.001,  step=0.0001,format="%.4f")

with right:
    st.markdown('<div class="section-title">🖼️ PIPE CROSS SECTION DIAGRAM</div>', unsafe_allow_html=True)

    # Draw pipe cross section diagram
    fig_diag, ax_diag = plt.subplots(figsize=(5, 4))
    ax_diag.set_facecolor('#0d1117')
    fig_diag.patch.set_facecolor('#0d1117')

    # Pipe outline (circle)
    pipe_outer = plt.Circle((0, 0), 1.0, color='#555555', fill=True, zorder=1)
    pipe_inner = plt.Circle((0, 0), 0.85, color='#1a3a5c', fill=True, zorder=2)
    flow_circle = plt.Circle((0, 0), 0.85, color='#1a3a5c', fill=True, zorder=2)
    ax_diag.add_patch(pipe_outer)
    ax_diag.add_patch(pipe_inner)

    # Flow arrows
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        ax_diag.annotate('', xy=(0.4*math.cos(rad), 0.4*math.sin(rad)),
                        xytext=(0, 0),
                        arrowprops=dict(arrowstyle='->', color='#00e5ff', lw=1.5))

    # Diameter arrow
    ax_diag.annotate('', xy=(1.0, 0), xytext=(-1.0, 0),
                    arrowprops=dict(arrowstyle='<->', color='#ff4444', lw=2))
    ax_diag.text(0, -1.2, f'D = {D:.3f} m', color='#ff4444',
                ha='center', va='center', fontsize=10, fontweight='bold')

    # Labels
    ax_diag.text(0, 0, 'FLOW', color='#00e5ff',
                ha='center', va='center', fontsize=11, fontweight='bold')
    ax_diag.text(0, 1.35, 'Pipe Cross Section', color='white',
                ha='center', fontsize=10, fontweight='bold')

    # Pipe wall label
    ax_diag.text(0.75, 0.75, 'Pipe\nWall', color='#aaaaaa',
                ha='center', fontsize=8)

    ax_diag.set_xlim(-1.6, 1.6)
    ax_diag.set_ylim(-1.6, 1.6)
    ax_diag.set_aspect('equal')
    ax_diag.axis('off')
    fig_diag.tight_layout()
    st.pyplot(fig_diag)
    plt.close(fig_diag)

    # Show current values summary
    st.markdown(f"""
    <div class="result-card">
    <b>📋 Current Input Summary</b><br>
    L = {L} m &nbsp;|&nbsp; D = {D} m &nbsp;|&nbsp; V = {V} m/s<br>
    ρ = {rho} kg/m³ &nbsp;|&nbsp; f = {f} &nbsp;|&nbsp; μ = {mu} Pa·s
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
if st.button("⚡  CALCULATE  ⚡", use_container_width=True):

    # ── Calculations ─────────────────────────────────────────────────────────
    Re      = (rho * V * D) / mu
    delta_P = f * (L / D) * 0.5 * rho * V**2
    Q       = math.pi * (D/2)**2 * V
    m_dot   = rho * Q
    v_head  = V**2 / (2 * 9.81)
    A       = math.pi * (D/2)**2

    regime = "Laminar"      if Re < 2300 else "Transitional" if Re < 4000 else "Turbulent"
    color  = "green"        if Re < 2300 else "orange"       if Re < 4000 else "red"
    emoji  = "🟢"           if Re < 2300 else "🟡"           if Re < 4000 else "🔴"

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📊 CALCULATION RESULTS</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="result-card {color}"><b>{emoji} Flow Regime</b><br>{regime}<br><small>Re = {Re:,.0f}</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><b>📐 Pipe Area</b><br>{A:.6f} m²</div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="result-card"><b>🔴 Pressure Drop (ΔP)</b><br>{delta_P:,.2f} Pa<br><small>{delta_P/1000:.4f} kPa</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><b>📏 Velocity Head</b><br>{v_head:.4f} m</div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="result-card"><b>💧 Flow Rate (Q)</b><br>{Q:.5f} m³/s<br><small>{Q*1000:.3f} L/s</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><b>⚖️ Mass Flow Rate</b><br>{m_dot:.3f} kg/s</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📈 GRAPHS & VISUALIZATIONS</div>', unsafe_allow_html=True)

    plt.style.use('dark_background')
    vel_range = np.linspace(0.1, max(V * 2.5, 5), 300)
    Re_range  = (rho * vel_range * D) / mu
    dP_range  = f * (L / D) * 0.5 * rho * vel_range**2
    len_range = np.linspace(1, max(L * 2.5, 20), 300)
    dP_len    = f * (len_range / D) * 0.5 * rho * V**2

    g1, g2 = st.columns(2)

    with g1:
        # Graph 1 — Pressure Drop vs Velocity
        fig1, ax1 = plt.subplots(figsize=(6, 3.8))
        ax1.plot(vel_range, dP_range, color='#00e5ff', linewidth=2.5)
        ax1.fill_between(vel_range, dP_range, alpha=0.15, color='#00e5ff')
        ax1.axvline(V, color='#ff4444', linestyle='--', lw=1.8, label=f'V = {V} m/s')
        ax1.axhline(delta_P, color='#ffab00', linestyle=':', lw=1.5, label=f'ΔP = {delta_P:.1f} Pa')
        ax1.scatter([V], [delta_P], color='#ff4444', s=120, zorder=6)
        ax1.set_xlabel('Velocity (m/s)', color='#aaa', fontsize=10)
        ax1.set_ylabel('Pressure Drop ΔP (Pa)', color='#aaa', fontsize=10)
        ax1.set_title('Pressure Drop vs Velocity', color='white', fontweight='bold', fontsize=12)
        ax1.legend(fontsize=9); ax1.grid(alpha=0.15)
        ax1.set_facecolor('#0d1117'); fig1.patch.set_facecolor('#0d1117')
        fig1.tight_layout(); st.pyplot(fig1); plt.close(fig1)

        # Graph 3 — Pressure Drop vs Pipe Length
        fig3, ax3 = plt.subplots(figsize=(6, 3.8))
        ax3.plot(len_range, dP_len, color='#ce93d8', linewidth=2.5)
        ax3.fill_between(len_range, dP_len, alpha=0.15, color='#ce93d8')
        ax3.axvline(L, color='#ff4444', linestyle='--', lw=1.8, label=f'L = {L} m')
        ax3.axhline(delta_P, color='#ffab00', linestyle=':', lw=1.5, label=f'ΔP = {delta_P:.1f} Pa')
        ax3.scatter([L], [delta_P], color='#ff4444', s=120, zorder=6)
        ax3.set_xlabel('Pipe Length (m)', color='#aaa', fontsize=10)
        ax3.set_ylabel('Pressure Drop ΔP (Pa)', color='#aaa', fontsize=10)
        ax3.set_title('Pressure Drop vs Pipe Length', color='white', fontweight='bold', fontsize=12)
        ax3.legend(fontsize=9); ax3.grid(alpha=0.15)
        ax3.set_facecolor('#0d1117'); fig3.patch.set_facecolor('#0d1117')
        fig3.tight_layout(); st.pyplot(fig3); plt.close(fig3)

    with g2:
        # Graph 2 — Reynolds Number vs Velocity (with zones)
        fig2, ax2 = plt.subplots(figsize=(6, 3.8))
        max_Re = max(Re_range) * 1.05
        ax2.fill_between(vel_range, 0,    2300,    alpha=0.25, color='#00e676', label='Laminar')
        ax2.fill_between(vel_range, 2300, 4000,    alpha=0.25, color='#ffab00', label='Transitional')
        ax2.fill_between(vel_range, 4000, max_Re,  alpha=0.2,  color='#ff1744', label='Turbulent')
        ax2.plot(vel_range, Re_range, color='#00e5ff', linewidth=2.5)
        ax2.axvline(V, color='#ff4444', linestyle='--', lw=1.8, label=f'V = {V} m/s')
        ax2.scatter([V], [Re], color='#ff4444', s=120, zorder=6)
        ax2.text(vel_range[10], 1000,  'LAMINAR',       color='#00e676', fontsize=8, alpha=0.8)
        ax2.text(vel_range[10], 2600,  'TRANSITIONAL',  color='#ffab00', fontsize=8, alpha=0.8)
        ax2.text(vel_range[10], 4500,  'TURBULENT',     color='#ff1744', fontsize=8, alpha=0.8)
        ax2.set_xlabel('Velocity (m/s)', color='#aaa', fontsize=10)
        ax2.set_ylabel('Reynolds Number (Re)', color='#aaa', fontsize=10)
        ax2.set_title('Reynolds Number vs Velocity', color='white', fontweight='bold', fontsize=12)
        ax2.legend(fontsize=9, loc='upper left'); ax2.grid(alpha=0.15)
        ax2.set_facecolor('#0d1117'); fig2.patch.set_facecolor('#0d1117')
        fig2.tight_layout(); st.pyplot(fig2); plt.close(fig2)

        # Graph 4 — Pipe Flow Profile (velocity profile)
        fig4, ax4 = plt.subplots(figsize=(6, 3.8))
        r = np.linspace(-D/2, D/2, 300)
        if Re < 2300:  # Laminar — parabolic
            v_profile = V * 2 * (1 - (r/(D/2))**2)
            profile_label = 'Laminar (Parabolic)'
            profile_color = '#00e676'
        else:          # Turbulent — flatter
            v_profile = V * 1.2 * (1 - np.abs(r/(D/2)))**(1/7)
            profile_label = 'Turbulent (Power Law)'
            profile_color = '#ff1744'
        ax4.plot(v_profile, r, color=profile_color, linewidth=2.5, label=profile_label)
        ax4.fill_betweenx(r, 0, v_profile, alpha=0.2, color=profile_color)
        ax4.axhline(D/2,  color='#888', linestyle='-', lw=2, label='Pipe Wall')
        ax4.axhline(-D/2, color='#888', linestyle='-', lw=2)
        ax4.axvline(0, color='#555', linestyle='--', lw=1)
        ax4.set_xlabel('Velocity (m/s)', color='#aaa', fontsize=10)
        ax4.set_ylabel('Radius (m)', color='#aaa', fontsize=10)
        ax4.set_title('Velocity Profile in Pipe', color='white', fontweight='bold', fontsize=12)
        ax4.legend(fontsize=9); ax4.grid(alpha=0.15)
        ax4.set_facecolor('#0d1117'); fig4.patch.set_facecolor('#0d1117')
        fig4.tight_layout(); st.pyplot(fig4); plt.close(fig4)

    with st.expander("📐 Formulas Used"):
        st.latex(r"Re = \frac{\rho V D}{\mu}")
        st.latex(r"\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho V^2}{2}")
        st.latex(r"Q = \frac{\pi D^2}{4} \cdot V \qquad \dot{m} = \rho Q")

st.markdown('<div class="footer">Group 10 · ICT Project · Fluid Mechanics Calculator</div>', unsafe_allow_html=True)
