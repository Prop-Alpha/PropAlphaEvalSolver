# This based on calculator from https://github.com/Prop-Alpha/PropAlphaEvalCalculator

import math
import streamlit as st
from winloss_graph import WinLossDiGraph
from PIL import Image

def calculate_probability(trailing_dd, account_target, stop_width, tp_width, win_pct):
    num_loss = math.ceil(trailing_dd / stop_width)
    num_win = math.ceil(account_target / stop_width)
    rr_ratio = round(tp_width / stop_width, 1)
    win_frac = win_pct / 100.0

    wldg = WinLossDiGraph()
    wldg.build_graph_from_start_node_and_params(win_frac, rr_ratio, num_win, num_loss)
    wldg.generate_adj_matrix()
    win_prob = wldg.get_win_prob_from_start_node() * 100

    return f"Estimated Probability of Success: {win_prob:.1f}%"


def run():
    image = Image.open('propalpha_logo.png')

    col1, col2, col3 = st.columns([6, 6, 6])

    with col1:
        st.write("")
    with col2:
        st.image(image, width=100)
    with col3:
        st.write("")


    st.title("Prop Alpha Eval Calculator")

    st.markdown("""
        Estimate odds of passing a prop eval with trailing drawdown given a single setup with a defined bracket and win percentage.\n
        Costs ignored.\n
        NOT FINANCIAL ADVICE. DO YOUR OWN RESEARCH. NO GUARANTEE OUR MATH IS CORRECT.\n
        RISK DISCLAIMER: [Read Here](https://www.prop-alpha.com/disclaimer)\n
    """)

    presets = {
        # Based on info from
        # https://support.apextraderfunding.com/hc/en-us/articles/4408610260507-How-Does-The-Trailing-Threshold-Work-Master-Course
        "Custom": {"trailing_dd": 0.0, "account_target": 0.0},
        "Apex 25k": {"trailing_dd": 1500.0, "account_target": 1500.0},
        "Apex 50k": {"trailing_dd": 2500.0, "account_target": 3000.0},
        "Apex 75k": {"trailing_dd": 2750.0, "account_target": 4250.0},
        "Apex 100k": {"trailing_dd": 3000.0, "account_target": 6000.0},
        "Apex 150k": {"trailing_dd": 5000.0, "account_target": 9000.0},
        "Apex 250k": {"trailing_dd": 6500.0, "account_target": 15000.0},
        "Apex 300k": {"trailing_dd": 7500.0, "account_target": 20000.0}
    }

    selected_preset = st.selectbox("Choose a preset or select Custom:", list(presets.keys()))

    with st.container():
        trailing_dd = st.number_input(
            "Enter Trailing Drawdown Amount in Currency",
            value=presets[selected_preset]["trailing_dd"],
            step=100.0
        )
        account_target = st.number_input(
            "Enter Account Target Amount in Currency",
            value=presets[selected_preset]["account_target"],
            step=100.0
        )
        stop_width = st.number_input("Enter Stop Size in Currency", value=100.0, step=100.0)
        tp_width = st.number_input("Enter Take Profit Size in Currency", value=0.0, step=100.0)
        win_pct = st.number_input("Enter Estimated Win Percent", value=0.0)

    compute_button = st.button("Compute Estimated Probability")

    # The following check ensures that the computation only happens when the button is pressed
    if compute_button:
        # Reserve a spot for our status message
        status_message = st.empty()

        # We can further check if all input fields are provided, although it's not strictly necessary since there are default values.
        if all([trailing_dd, account_target, stop_width, tp_width, win_pct]):
            # Display a message saying the computation is running
            status_message.text("Computing... Please wait.")

            result = calculate_probability(trailing_dd, account_target, stop_width, tp_width, win_pct)
            status_message.markdown(f"### {result}")
        else:
            st.warning("Please provide all input values before computing.")


if __name__ == '__main__':
    run()