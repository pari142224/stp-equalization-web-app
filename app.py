import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Equalization Tank Design Tool", layout="wide")

st.title("Equalization Tank Design (Hourly Flow Based)")

st.header("Enter 24 Hourly Flow Data (L/min)")

hours = list(range(1, 25))
flow_data = []

cols = st.columns(4)

for i in range(24):
    with cols[i % 4]:
        value = st.number_input(f"Hour {i+1}", min_value=0.0, value=3000.0, key=i)
        flow_data.append(value)

depth_eq = st.sidebar.number_input("EQ Tank Water Depth (m)", value=4.0)
air_rate = st.sidebar.number_input("Air Rate (m³/min per m³)", value=0.012)

if st.button("Calculate Equalization Tank"):

    # Convert L/min to m3/hr
    flow_m3hr = np.array(flow_data) * 0.06

    # Total & Average
    total_daily_flow = sum(flow_m3hr)
    avg_hourly = np.mean(flow_m3hr)
    peak_hour = max(flow_m3hr)

    peak_factor = peak_hour / avg_hourly

    # Deviation
    deviation = flow_m3hr - avg_hourly
    cumulative = np.cumsum(deviation)

    eq_volume = max(cumulative) - min(cumulative)

    # Tank Dimensions (L:W = 2:1)
    area_eq = eq_volume / depth_eq
    width_eq = math.sqrt(area_eq / 2)
    length_eq = 2 * width_eq

    # Blower Requirement
    air_required = eq_volume * air_rate

    # ----------------------------
    # RESULTS
    # ----------------------------
    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Flow Analysis")
        st.write("Total Daily Flow (m³/day):", round(total_daily_flow,2))
        st.write("Average Hourly Flow (m³/hr):", round(avg_hourly,2))
        st.write("Peak Hourly Flow (m³/hr):", round(peak_hour,2))
        st.write("Peak Factor:", round(peak_factor,2))

    with col2:
        st.subheader("Equalization Tank Design")
        st.write("Required Volume (m³):", round(eq_volume,2))
        st.write("Suggested Length (m):", round(length_eq,2))
        st.write("Suggested Width (m):", round(width_eq,2))
        st.write("Water Depth (m):", depth_eq)
        st.write("Air Required (m³/min):", round(air_required,2))

    # ----------------------------
    # MASS CURVE
    # ----------------------------
    st.subheader("Mass Curve (Ripple Diagram)")

    fig = plt.figure()
    plt.plot(hours, cumulative)
    plt.xlabel("Hour")
    plt.ylabel("Cumulative Deviation (m³)")
    st.pyplot(fig)

    st.success("Equalization Tank Designed Successfully")