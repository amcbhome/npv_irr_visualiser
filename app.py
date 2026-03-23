import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 IRR Interpolation Visualiser")

st.markdown("This app plots two NPV points and estimates IRR using interpolation.")

# -----------------------------
# User Inputs
# -----------------------------
st.header("Inputs")

initial_investment = st.number_input("Initial Investment (£)", value=50000)

cash_flows_input = st.text_input(
    "Cash Flows (comma separated)",
    "10000,10000,10000,10000,10000"
)

rate1 = st.number_input("Discount Rate 1 (%)", value=8.0)
rate2 = st.number_input("Discount Rate 2 (%)", value=12.0)

# Convert inputs
cash_flows = [float(x.strip()) for x in cash_flows_input.split(",")]

# -----------------------------
# NPV Function
# -----------------------------
def calculate_npv(rate, initial, flows):
    npv = -initial
    for t, cf in enumerate(flows, start=1):
        npv += cf / (1 + rate) ** t
    return npv

# -----------------------------
# Calculate NPVs
# -----------------------------
r1 = rate1 / 100
r2 = rate2 / 100

npv1 = calculate_npv(r1, initial_investment, cash_flows)
npv2 = calculate_npv(r2, initial_investment, cash_flows)

# -----------------------------
# IRR Interpolation
# -----------------------------
irr_est = r1 + (npv1 / (npv1 - npv2)) * (r2 - r1)

# -----------------------------
# Output Results
# -----------------------------
st.header("Results")

st.write(f"NPV at {rate1}%: £{npv1:,.2f}")
st.write(f"NPV at {rate2}%: £{npv2:,.2f}")
st.write(f"Estimated IRR: {irr_est * 100:.2f}%")

# -----------------------------
# Plot Graph
# -----------------------------
st.header("Graph")

# Points
rates = [rate1, rate2]
npvs = [npv1, npv2]

# Line for interpolation
x_line = np.linspace(rate1, rate2, 100)
y_line = npv1 + (npv2 - npv1) * (x_line - rate1) / (rate2 - rate1)

# Plot
fig, ax = plt.subplots()

# Scatter points
ax.scatter(rates, npvs, label="NPV Points")

# Interpolation line
ax.plot(x_line, y_line, linestyle="--", label="Interpolation")

# Zero line
ax.axhline(0)

# IRR vertical line
ax.axvline(irr_est * 100, linestyle=":", label="Estimated IRR")

# Labels
ax.set_xlabel("Discount Rate (%)")
ax.set_ylabel("NPV (£)")
ax.set_title("IRR Interpolation")

ax.legend()

st.pyplot(fig)
