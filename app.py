
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from simulator import simulate_net_metering


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Home Microgrid Simulator",
    page_icon="☀️",
    layout="wide"
)


# ==========================================
# 2. APPLICATION TITLE
# ==========================================

st.title("☀️ Home Microgrid / Net-Metering Simulator")

st.subheader("Rooftop Solar Energy and Financial Analysis")

st.write(
    "This application simulates household electricity "
    "consumption, solar generation, grid imports, "
    "grid exports and financial savings."
)

st.info(
    "This project uses illustrative 14-day sample data. "
    "Results are estimates, not actual household measurements."
)


# ==========================================
# 3. LOAD CLEANED DATASET
# ==========================================

data = pd.read_csv("data/cleaned_dataset.csv")


# ==========================================
# 4. SIDEBAR - SIMULATION PARAMETERS
# ==========================================

st.sidebar.header("Simulation Parameters")

import_tariff = st.sidebar.number_input(
    "Grid Import Tariff (₹/kWh)",
    min_value=0.0,
    value=8.0,
    step=0.5
)

export_tariff = st.sidebar.number_input(
    "Export Tariff (₹/kWh)",
    min_value=0.0,
    value=3.0,
    step=0.5
)

installation_cost = st.sidebar.number_input(
    "Solar Installation Cost (₹)",
    min_value=0,
    value=180000,
    step=5000
)


# ==========================================
# 5. RUN NET-METERING SIMULATION
# ==========================================

results = simulate_net_metering(
    data.copy(),
    import_tariff,
    export_tariff,
    installation_cost
)


# Calculate daily energy distribution for dashboard
data["self_consumption_kwh"] = data.apply(
    lambda row: min(
        row["household_consumption_kwh"],
        row["solar_generation_kwh"]
    ),
    axis=1
)

data["grid_import_kwh"] = (
    data["household_consumption_kwh"]
    - data["solar_generation_kwh"]
).clip(lower=0)

data["grid_export_kwh"] = (
    data["solar_generation_kwh"]
    - data["household_consumption_kwh"]
).clip(lower=0)



# ==========================================
# 6. ENERGY OVERVIEW
# ==========================================

st.header("Energy Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Consumption",
    f"{results['Total Consumption (kWh)']:.2f} kWh"
)

col2.metric(
    "Solar Generation",
    f"{results['Total Solar Generation (kWh)']:.2f} kWh"
)

col3.metric(
    "Solar Self-Consumption",
    f"{results['Solar Self-Consumption (kWh)']:.2f} kWh"
)


# ==========================================
# 7. GRID IMPORT AND EXPORT
# ==========================================

st.header("Grid Import and Export")

col4, col5 = st.columns(2)

col4.metric(
    "Grid Import",
    f"{results['Grid Import (kWh)']:.2f} kWh"
)

col5.metric(
    "Grid Export",
    f"{results['Grid Export (kWh)']:.2f} kWh"
)


# ==========================================
# 8. FINANCIAL ANALYSIS
# ==========================================

st.header("Financial Analysis")

col6, col7, col8 = st.columns(3)

col6.metric(
    "Original Electricity Bill",
    f"₹{results['Original Electricity Bill (Rs)']:.2f}"
)

col7.metric(
    "Solar Electricity Bill",
    f"₹{results['Solar Electricity Bill (Rs)']:.2f}"
)

col8.metric(
    "14-Day Savings",
    f"₹{results['Savings (Rs)']:.2f}"
)


# ==========================================
# 9. SOLAR INVESTMENT ANALYSIS
# ==========================================

st.header("Solar Investment Analysis")

col9, col10 = st.columns(2)

col9.metric(
    "Estimated Annual Savings",
    f"₹{results['Estimated Annual Savings (Rs)']:,.2f}"
)

payback = results["Payback Period (Years)"]

col10.metric(
    "Estimated Payback Period",
    f"{payback:.2f} Years"
    if payback is not None
    else "Not achieved"
)

st.caption(
    "Payback is a simple estimate based on annualised "
    "14-day savings. Actual performance may vary."
)


# ==========================================
# 10. DAILY CONSUMPTION VS SOLAR GENERATION
# ==========================================

st.header("Daily Consumption vs Solar Generation")

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    data["date"],
    data["household_consumption_kwh"],
    marker="o",
    label="Household Consumption"
)

ax.plot(
    data["date"],
    data["solar_generation_kwh"],
    marker="o",
    label="Solar Generation"
)

ax.set_xlabel("Date")
ax.set_ylabel("Energy (kWh)")
ax.set_title("Daily Energy Comparison")
ax.legend()
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)


# ==========================================
# 11. GRID ENERGY DISTRIBUTION
# ==========================================

st.header("Grid Energy Distribution")

fig, ax = plt.subplots()

ax.bar(
    ["Grid Import", "Grid Export"],
    [
        results["Grid Import (kWh)"],
        results["Grid Export (kWh)"]
    ]
)

ax.set_ylabel("Energy (kWh)")
ax.set_title("Grid Import vs Export")

st.pyplot(fig)
plt.close(fig)


# ==========================================
# 12. ELECTRICITY BILL COMPARISON
# ==========================================

st.header("Electricity Bill Comparison")

fig, ax = plt.subplots()

ax.bar(
    ["Without Solar", "With Solar"],
    [
        results["Original Electricity Bill (Rs)"],
        results["Solar Electricity Bill (Rs)"]
    ]
)

ax.set_ylabel("Amount (₹)")
ax.set_title("Electricity Bill Before and After Solar")

st.pyplot(fig)
plt.close(fig)


# ==========================================
# 13. DAILY SIMULATION RESULTS TABLE
# ==========================================

st.header("Daily Simulation Results")

st.write(
    "The following table presents daily household "
    "energy consumption, solar generation and grid interaction."
)

daily_results = data[
    [
        "date",
        "household_consumption_kwh",
        "solar_generation_kwh",
        "self_consumption_kwh",
        "grid_import_kwh",
        "grid_export_kwh"
    ]
].copy()

daily_results.columns = [
    "Date",
    "Consumption (kWh)",
    "Solar Generation (kWh)",
    "Self Consumption (kWh)",
    "Grid Import (kWh)",
    "Grid Export (kWh)"
]

st.dataframe(
    daily_results.round(2),
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 14. DOWNLOAD SIMULATION RESULTS
# ==========================================

st.subheader("Download Simulation Data")

csv_data = daily_results.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Daily Results CSV",
    data=csv_data,
    file_name="microgrid_simulation_results.csv",
    mime="text/csv"
)


# ==========================================
# 15. PROJECT CONCLUSION
# ==========================================

st.header("Project Conclusion")

if payback is not None:

    st.success(
        f"Based on the illustrative dataset, rooftop solar "
        f"produces estimated annual savings of "
        f"₹{results['Estimated Annual Savings (Rs)']:,.2f} "
        f"with a simple payback period of {payback:.2f} years."
    )

else:

    st.warning(
        "The solar installation cost is not recovered "
        "under the current simulation assumptions."
    )


st.caption(
    "Note: This is an educational simulation. Actual "
    "electricity tariffs, net-metering policies, seasonal "
    "variations, maintenance costs and solar system "
    "performance must be considered before installation."
)

