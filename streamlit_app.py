# this is an adaptation of Vespatrades's work here:
# https://github.com/vespatrades/PropAlphaEvalCalculator_Streamlit/blob/master/streamlit_app.py

import streamlit as st
from PIL import Image
from simulation import Simulation
from trading_strategies import TradingStrategy


def run():
    image = Image.open('propalpha_logo.png')

    col1, col2, col3 = st.columns([6, 6, 6])

    with col1:
        st.write("")
    with col2:
        st.image(image, width=100)
    with col3:
        st.write("")

    st.title("Prop Alpha Eval Solver")

    st.markdown("""
        Estimate expected value of a full payout in prop accounts with EOD trailing drawdown \n
        given a single setup with a defined bracket and known win percentage and average mfe.\n
        NOT FINANCIAL ADVICE. \n
        DO YOUR OWN RESEARCH. \n
        NO GUARANTEE OUR MATH IS CORRECT. \n
        RISK DISCLAIMER: https://www.prop-alpha.com/disclaimer
    """)

    account_rule_presets = {
        "Topstep 50k": {'Initial Balance (Eval)': 50000, 'Initial Balance (Funded)': 50000, 'Max Loss (Eval)': 2000,
                        'Max Loss (Funded)': 2000, 'Funding Target Balance': 53000,
                        'Unshared Winning Balance (Funded)': 60000,
                        'Profit Share Fraction': .9, 'Winning Day PnL Minimum': 200, 'Maximum Daily Loss': 1000,
                        'Maximum Daily Win': 1500, 'Minimum Winning Days for Payout': 30,
                        'Minimum Winning Balance': 60000
                        },
        "Topstep 100k": {'Initial Balance (Eval)': 100000, 'Initial Balance (Funded)': 100000, 'Max Loss (Eval)': 3000,
                         'Max Loss (Funded)': 3000, 'Funding Target Balance': 106000,
                         'Unshared Winning Balance (Funded)': 110000,
                         'Profit Share Fraction': .9, 'Winning Day PnL Minimum': 200, 'Maximum Daily Loss': 2000,
                         'Maximum Daily Win': 4500, 'Minimum Winning Days for Payout': 30,
                         'Minimum Winning Balance': 110000
                         },
        "Topstep 150k": {'Initial Balance (Eval)': 150000, 'Initial Balance (Funded)': 150000, 'Max Loss (Eval)': 4500,
                         'Max Loss (Funded)': 4500, 'Funding Target Balance': 159000,
                         'Unshared Winning Balance (Funded)': 160000,
                         'Profit Share Fraction': .9, 'Winning Day PnL Minimum': 200, 'Maximum Daily Loss': 3000,
                         'Maximum Daily Win': 4500, 'Minimum Winning Days for Payout': 30,
                         'Minimum Winning Balance': 160000
                         }
    }
    cost_fee_preset = {
        "Custom": {
            "Eval Acct Cost": 0,
            "Funded Acct Setup Cost": 0,
            "Per Side Trade Cost": 0,
            "Trade Entry Slippage": 0,
            "Trade Stop Slippage": 0,
            "Monthly Funded Account Cost": 0
        },
        "Topstep": {
            "Eval Acct Cost": 149,
            "Funded Acct Setup Cost": 149,
            "Per Side Trade Cost": 2,
            "Trade Entry Slippage": 0,
            "Trade Stop Slippage": 10,
            "Monthly Funded Account Cost": 0
        }
    }

    selected_acct_preset = st.selectbox("Choose an account preset:", list(account_rule_presets.keys()))
    selected_fee_preset = st.selectbox("Choose a cost/fee preset or select Custom:", list(cost_fee_preset.keys()))

    with st.container():
        eval_cost = st.number_input("Enter Eval Account Cost",
                                    value=cost_fee_preset[selected_fee_preset]["Eval Acct Cost"], step=1)
        funded_cost = st.number_input("Enter Funded Account Setup Cost",
                                      value=cost_fee_preset[selected_fee_preset]["Funded Acct Setup Cost"], step=1)
        per_side_cost = st.number_input("Enter Per Side Trade Cost",
                                        value=cost_fee_preset[selected_fee_preset]["Per Side Trade Cost"])
        trade_entry_slippage = st.number_input("Enter Trade Entry Slippage Estimate",
                                               value=cost_fee_preset[selected_fee_preset]["Trade Entry Slippage"])
        trade_stop_slippage = st.number_input("Enter Stop Loss Slippage Estimate",
                                              value=cost_fee_preset[selected_fee_preset]["Trade Stop Slippage"])
        monthly_cost = st.number_input("Enter Monthly Funded Account Cost",
                                       value=cost_fee_preset[selected_fee_preset]["Monthly Funded Account Cost"])
        fees = {
            "Eval Acct Cost": eval_cost,
            "Funded Acct Setup Cost": funded_cost,
            "Per Side Trade Cost": per_side_cost,
            "Trade Entry Slippage": trade_entry_slippage,
            "Trade Stop Slippage": trade_stop_slippage,
            "Monthly Funded Account Cost": monthly_cost
        }
        stop_width = st.number_input("Enter Stop Size in Currency", value=3000)
        tp_width = st.number_input("Enter Take Profit Size in Currency", value=3000)
        win_pct = st.number_input("Enter Estimated Win Percent", value=50.0)
        mfe = st.number_input("Enter Estimated MFE (of Losing Trades) in Currency", value=500)
        trades_per_day = st.number_input("Enter Number of Trades Per Day", value=3)
        win_pct /= 100
        monte_carlo_runs = st.number_input("Enter Number of Runs in Simulation", value=20000)

    compute_button = st.button("Compute Estimated Probability")

    # The following check ensures that the computation only happens when the button is pressed
    if compute_button:
        # Reserve a spot for our status message
        status_message = st.empty()

        # We can further check if all input fields are provided, although it's not strictly necessary since there are
        # default values.
        if all([trades_per_day, stop_width, tp_width, win_pct]):
            # Display a message saying the computation is running
            status_message.text("Computing... Please wait.")
            strategy = TradingStrategy(odds=win_pct, mfe=mfe, trades_per_day=trades_per_day,
                                       stop_width=stop_width, tp_width=tp_width)
            sim = Simulation(trading_strat=strategy, num_traders=int(monte_carlo_runs),
                             acct_rules=account_rule_presets[selected_acct_preset], acct_fees=fees)
            sim.run()
            result = sim.sim_results()
            status_message.markdown(f"### {result}")
        else:
            st.warning("Please provide all input values before computing.")


if __name__ == '__main__':
    run()
