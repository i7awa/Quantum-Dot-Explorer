import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ==========================================
# QUANTUM DOT EXPLORER
# Medical Fluorescence + QLED Display
# ==========================================

st.set_page_config(
    page_title="Quantum Dot Explorer",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Quantum Dot Explorer")
st.markdown(
    "Interactive simulation of Quantum Dots "
    "for medical fluorescence and QLED displays."
)

st.sidebar.title("Simulation Control")

application = st.sidebar.selectbox(
    "Choose Application",
    [
        "Medical Application",
        "QLED Display"
    ]
)

# ==========================================
# PHYSICAL MODEL: BRUS EQUATION
# ==========================================

HBAR = 1.054571817e-34
M_E = 9.1093837e-31
Q = 1.602176634e-19
EPSILON_0 = 8.8541878128e-12
H = 6.62607015e-34
C = 299792458

BULK_GAP = 1.74
ELECTRON_MASS = 0.13
HOLE_MASS = 0.45
EPSILON_R = 9.5


def calculate_quantum_dot(radius_nm):

    radius = radius_nm * 1e-9

    electron_energy = (
        HBAR**2 * math.pi**2
        / (2 * ELECTRON_MASS * M_E * radius**2)
    ) / Q

    hole_energy = (
        HBAR**2 * math.pi**2
        / (2 * HOLE_MASS * M_E * radius**2)
    ) / Q

    coulomb_energy = (
        1.8 * Q**2
        / (4 * math.pi * EPSILON_0
           * EPSILON_R * radius)
    ) / Q

    exciton_energy = (
        BULK_GAP
        + electron_energy
        + hole_energy
        - coulomb_energy
    )

    wavelength = (
        H * C
        / (exciton_energy * Q)
    ) * 1e9

    return (
        electron_energy,
        hole_energy,
        coulomb_energy,
        exciton_energy,
        wavelength
    )


def wavelength_to_color(wavelength):

    if wavelength < 380 or wavelength > 780:
        return "#888888"

    if wavelength < 440:
        return "#7040FF"
    elif wavelength < 490:
        return "#008CFF"
    elif wavelength < 510:
        return "#00DDAA"
    elif wavelength < 580:
        return "#65DD30"
    elif wavelength < 645:
        return "#FFB000"
    else:
        return "#FF3030"


def wavelength_region(wavelength):

    if wavelength < 380:
        return "Ultraviolet"
    elif wavelength < 450:
        return "Violet"
    elif wavelength < 495:
        return "Blue"
    elif wavelength < 570:
        return "Green"
    elif wavelength < 590:
        return "Yellow"
    elif wavelength < 620:
        return "Orange"
    elif wavelength <= 780:
        return "Red"
    else:
        return "Infrared"


# ==========================================
# MEDICAL APPLICATION
# ==========================================

if application == "Medical Application":

    st.header("🧬 Medical Fluorescence Imaging")

    st.write(
        "Study how quantum dot size and "
        "targeting conditions affect fluorescence signals."
    )

    col1, col2 = st.columns(2)

    with col1:
        radius = st.slider(
            "Quantum Dot Radius (nm)",
            1.5, 5.0, 3.0, 0.1
        )

        concentration = st.slider(
            "Quantum Dot Concentration (nM)",
            1.0, 100.0, 30.0, 1.0
        )

    with col2:
        targeting = st.slider(
            "Targeting Efficiency",
            0.0, 1.0, 0.85, 0.05
        )

        quantum_yield = st.slider(
            "Fluorescence Quantum Yield",
            0.1, 1.0, 0.75, 0.05
        )

    electron, hole, binding, energy, wavelength = (
        calculate_quantum_dot(radius)
    )

    st.subheader("Quantum Dot Physical Properties")

    m1, m2, m3 = st.columns(3)

    m1.metric("Exciton Transition Energy", f"{energy:.3f} eV")
    m2.metric("Emission Wavelength", f"{wavelength:.1f} nm")
    m3.metric("Emission Region", wavelength_region(wavelength))

    st.markdown("---")
    st.subheader("Fluorescence Signal Simulation")

    kd = 20.0
    occupancy = concentration / (concentration + kd)

    nonspecific = 0.08

    tumor_signal = (
        quantum_yield
        * (nonspecific + targeting * occupancy)
        * 100
    )

    normal_signal = (
        quantum_yield
        * nonspecific
        * 100
    )

    contrast = tumor_signal / max(normal_signal, 0.001)

    a, b, c = st.columns(3)

    a.metric("Tumor Signal", f"{tumor_signal:.2f}")
    b.metric("Normal Signal", f"{normal_signal:.2f}")
    c.metric("Signal Contrast", f"{contrast:.2f} x")

    concentrations = np.linspace(1, 100, 100)

    tumor_values = []
    normal_values = []

    for value in concentrations:

        occ = value / (value + kd)

        tumor_values.append(
            quantum_yield
            * (nonspecific + targeting * occ)
            * 100
        )

        normal_values.append(
            quantum_yield * nonspecific * 100
        )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=concentrations,
        y=tumor_values,
        mode="lines",
        name="Tumor Cells"
    ))

    fig.add_trace(go.Scatter(
        x=concentrations,
        y=normal_values,
        mode="lines",
        name="Normal Cells"
    ))

    fig.update_layout(
        title="Fluorescence Signal vs Concentration",
        xaxis_title="Concentration (nM)",
        yaxis_title="Relative Fluorescence Signal",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "This is a simplified theoretical model. "
        "It illustrates targeted fluorescence and is not "
        "a validated medical diagnostic system."
    )


# ==========================================
# QLED DISPLAY APPLICATION
# ==========================================

elif application == "QLED Display":

    st.header("🖥️ Quantum Dot LED Display")

    st.write(
        "Explore how quantum dot size controls "
        "the emitted light and display colour."
    )

    st.subheader("Choose Quantum Dot Sizes")

    col1, col2, col3 = st.columns(3)

    with col1:
        red_radius = st.slider(
            "Red Quantum Dot Radius (nm)",
            1.5, 5.0, 4.0, 0.1
        )

    with col2:
        green_radius = st.slider(
            "Green Quantum Dot Radius (nm)",
            1.5, 5.0, 3.0, 0.1
        )

    with col3:
        blue_radius = st.slider(
            "Blue Quantum Dot Radius (nm)",
            1.5, 5.0, 2.0, 0.1
        )

    colors_data = [
        ("Red", red_radius),
        ("Green", green_radius),
        ("Blue", blue_radius)
    ]

    st.subheader("Emission Results")

    result_columns = st.columns(3)

    for i, (name, radius) in enumerate(colors_data):

        _, _, _, energy, wavelength = (
            calculate_quantum_dot(radius)
        )

        color = wavelength_to_color(wavelength)

        with result_columns[i]:

            st.markdown(f"### {name}")

            st.markdown(
                f"""
                <div style="
                    background:{color};
                    height:90px;
                    border-radius:12px;
                    margin-bottom:12px;
                "></div>
                """,
                unsafe_allow_html=True
            )

            st.metric("Radius", f"{radius:.1f} nm")
            st.metric("Transition Energy", f"{energy:.3f} eV")
            st.metric("Wavelength", f"{wavelength:.1f} nm")
            st.write(wavelength_region(wavelength))

    st.markdown("---")
    st.subheader("Energy vs Quantum Dot Radius")

    radii = np.linspace(1.5, 5.0, 100)

    energies = [
        calculate_quantum_dot(r)[3]
        for r in radii
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=radii,
        y=energies,
        mode="lines",
        name="Exciton Transition Energy"
    ))

    fig.update_layout(
        title="Quantum Confinement Effect",
        xaxis_title="Quantum Dot Radius (nm)",
        yaxis_title="Transition Energy (eV)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Emission Spectrum")

    selected_radius = st.slider(
        "Select a Dot Radius for Spectrum (nm)",
        1.5, 5.0, 3.0, 0.1,
        key="spectrum_radius"
    )

    _, _, _, selected_energy, selected_wavelength = (
        calculate_quantum_dot(selected_radius)
    )

    x = np.linspace(380, 780, 500)

    width = 18

    intensity = np.exp(
        -0.5 * ((x - selected_wavelength) / width)**2
    )

    spectrum = go.Figure()

    spectrum.add_trace(go.Scatter(
        x=x,
        y=intensity,
        mode="lines",
        fill="tozeroy",
        name="Emission Spectrum"
    ))

    spectrum.update_layout(
        title="Quantum Dot Emission Spectrum",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Relative Intensity",
        template="plotly_dark"
    )

    st.plotly_chart(
        spectrum,
        use_container_width=True
    )


# ==========================================
# PHYSICS INFORMATION
# ==========================================

with st.expander("📘 Physical Model and Equations"):

    st.markdown("""
    **Brus Equation – Simplified Spherical Quantum Dot Model**

    The exciton transition energy is calculated as:

    E = Eg + Ee + Eh - Ec

    Where:

    - Eg: Bulk band gap energy
    - Ee: Electron confinement energy
    - Eh: Hole confinement energy
    - Ec: Electron-hole Coulomb attraction

    The emitted photon wavelength is:

    λ = hc / E

    Smaller quantum dots generally have higher
    confinement energy and shorter emission wavelengths.
    """)

st.caption(
    "Quantum Dot Explorer | Educational Physics Simulation"
)