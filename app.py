import streamlit as st

st.title("💧 Pipe Flow & Pressure Drop Calculator")
st.write("Group 10 - ICT Project")

# Inputs
L = st.number_input("Pipe Length (m)", min_value=0.1, value=10.0)
D = st.number_input("Pipe Diameter (m)", min_value=0.01, value=0.1)
v = st.number_input("Fluid Velocity (m/s)", min_value=0.0, value=1.5)
rho = st.number_input("Fluid Density (kg/m³)", min_value=1.0, value=1000.0)
f = st.slider("Friction Factor (f)", 0.001, 0.100, 0.020)

# Calculation
if st.button("Calculate Pressure Drop"):
    # Darcy-Weisbach Equation
    delta_p = f * (L / D) * (rho * (v**2) / 2)
    st.success(f"### Total Pressure Drop: {delta_p:.2f} Pascals")
