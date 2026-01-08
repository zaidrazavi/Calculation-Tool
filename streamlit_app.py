import streamlit as st
from logic import calculate

st.set_page_config(
    page_title="Calculation Tool",
    page_icon="",
    layout="centered"
)

st.title("Calculation Tool")
st.write("Enter budget and select BHK. Cost will be auto-distributed.")

# INPUTS
budget = st.number_input(
    "Enter Total Budget (₹)",
    min_value=25000,
    step=1000,
    format="%d"
)

bhk = st.selectbox(
    "Select BHK Type",
    ["1BHK", "2BHK", "3BHK"]
)

# BUTTON
if st.button("Generate Cost"):
    if budget <= 0:
        st.error("Please enter a valid budget")
    else:
        result = calculate(budget, bhk)

        st.success("Cost Generated Successfully")

        st.subheader(f"BHK: {result['BHK']}")
        st.subheader(f"Budget: ₹{result['Budget']:,}")

        st.divider()

        total = 0
        for item, amount in result["Breakdown"].items():
            st.write(f"**{item}** : ₹{amount:,}")
            total += amount

        st.divider()
        st.subheader(f"TOTAL: ₹{total:,}")

# HISTORY
st.divider()
st.subheader("🕒 Last 5 Calculations")

from logic import history

for idx, h in enumerate(history, 1):
    with st.expander(f"{idx}) ₹{h['Budget']:,} | {h['BHK']} | {len(h['Breakdown'])} items"):
        subtotal = 0
        for item, amount in h["Breakdown"].items():
            st.write(f"- **{item}** : ₹{amount:,}")
            subtotal += amount

        st.markdown(f"**Subtotal:** ₹{subtotal:,}")



