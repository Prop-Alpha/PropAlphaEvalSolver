# this is an adaptation of Vespatrades's work here:
# https://github.com/vespatrades/PropAlphaEvalCalculator_Streamlit/blob/master/streamlit_app.py

import streamlit as st
from simulation import Simulation
from trading_strategies import TradingStrategy

account_rule_presets = {
    "Topstep 50k": {'Initial Balance (Eval)': 50000,
                    'Initial Balance (Funded)': 50000,
                    'Max Loss (Eval)': 2000,
                    'Max Loss (Funded)': 2000,
                    'Funding Target Balance': 53000,
                    'Unshared Winning Balance (Funded)': 60000,
                    'Profit Share Fraction': .9,
                    'Winning Day PnL Minimum': 200,
                    'Maximum Daily Loss': 1000,
                    'Maximum Daily Win': 1500,
                    'Minimum Winning Days for Payout': 30,
                    'Minimum Winning Balance': 60000
                    },
    "Topstep 100k": {'Initial Balance (Eval)': 100000,
                     'Initial Balance (Funded)': 100000,
                     'Max Loss (Eval)': 3000,
                     'Max Loss (Funded)': 3000,
                     'Funding Target Balance': 106000,
                     'Unshared Winning Balance (Funded)': 110000,
                     'Profit Share Fraction': .9,
                     'Winning Day PnL Minimum': 200,
                     'Maximum Daily Loss': 2000,
                     'Maximum Daily Win': 4500,
                     'Minimum Winning Days for Payout': 30,
                     'Minimum Winning Balance': 110000
                     },
    "Topstep 150k": {'Initial Balance (Eval)': 150000,
                     'Initial Balance (Funded)': 150000,
                     'Max Loss (Eval)': 4500,
                     'Max Loss (Funded)': 4500,
                     'Funding Target Balance': 159000,
                     'Unshared Winning Balance (Funded)': 160000,
                     'Profit Share Fraction': .9,
                     'Winning Day PnL Minimum': 200,
                     'Maximum Daily Loss': 3000,
                     'Maximum Daily Win': 4500,
                     'Minimum Winning Days for Payout': 30,
                     'Minimum Winning Balance': 160000
                     },
    "Custom...": {'Initial Balance (Eval)': 0,
                  'Initial Balance (Funded)': 0,
                  'Max Loss (Eval)': 0,
                  'Max Loss (Funded)': 0,
                  'Funding Target Balance': 0,
                  'Unshared Winning Balance (Funded)': 0,
                  'Profit Share Fraction': 0.0,
                  'Winning Day PnL Minimum': 0,
                  'Maximum Daily Loss': 0,
                  'Maximum Daily Win': 0,
                  'Minimum Winning Days for Payout': 0,
                  'Minimum Winning Balance': 0
                  }
}
cost_fee_preset = {
    "Topstep": {
        "Eval Acct Cost": 149,
        "Funded Acct Setup Cost": 149,
        "Per Side Trade Cost": 0,
        "Trade Entry Slippage": 0,
        "Trade Stop Slippage": 0,
        "Monthly Funded Account Cost": 0
    },
    "Custom...": {
        "Eval Acct Cost": 0,
        "Funded Acct Setup Cost": 0,
        "Per Side Trade Cost": 0,
        "Trade Entry Slippage": 0,
        "Trade Stop Slippage": 0,
        "Monthly Funded Account Cost": 0
    }
}


def run():
    with st.container():
        # --- Main Elements --- #
        st.markdown(
            '<a href="https://www.prop-alpha.com/" target="_blank">'
            '<img src="./app/static/propalpha_banner.png" width="715">'
            '</a>',
            unsafe_allow_html=True,
        )

        st.title("Prop Alpha Eval Solver")

        st.markdown('''
            Estimate the expected full payout value for prop trading accounts, given 
            costs, fees, rules, and a trade strategy. Factors in EOD trailing 
            drawdown. Strategy includes defined order bracket, win rate, and average MFE.\n

            NOT FINANCIAL ADVICE.  
            DO YOUR OWN RESEARCH.  
            NO GUARANTEE OUR MATH IS CORRECT.  
            RISK DISCLAIMER: https://www.prop-alpha.com/disclaimer
        ''')
        st.divider()
        st.subheader('Trade Strategy')
        stop_width = st.number_input(label="Enter Stop Size in Currency", help="Stop loss in dollars", value=3000,
                                     step=100)

        tp_width = st.number_input(label="Enter Take Profit Size in Currency", help="Take profit in dollars",
                                   value=3000, step=100)

        win_pct = st.number_input(label="Enter Estimated Win Percent", help="", value=50.0, step=0.1)
        win_pct /= 100  # convert the percentage value into a proportion

        mfe = st.number_input(label="Enter Estimated MFE (of Losing Trades) in Currency", value=500, step=10)

        trades_per_day = st.number_input(label="Enter Number of Trades Per Day",
                                         help="Number of trades strategy takes in a single day", value=3, step=1)

        monte_carlo_runs = st.number_input("Enter Number of Runs in Simulation", value=20000, step=1000)

    compute_button = st.button("Compute Results")

    # --- Sidebar Elements --- #
    with st.sidebar:
        st.markdown("# Account Rules")
        selected_acct_preset = st.selectbox(label="Presets", label_visibility="hidden", index=2, options=list(account_rule_presets.keys()))
        with st.expander("Advanced Account Rules Input"):
            # Dynamically generate inputs based on the keys in the selected preset
            rules = {}
            for key, default_value in account_rule_presets[selected_acct_preset].items():
                # Determine step size based on the key (this can be refined)
                step_size = 0.1 if "Fraction" in key else 100
                rules[key] = st.number_input(key, value=default_value, step=step_size)

        st.divider()
        st.markdown("# Account Costs/Fees")
        selected_fee_preset = st.selectbox(label="Presets", label_visibility="hidden", index=-0, options=list(cost_fee_preset.keys()))

        with st.expander("Advanced Cost/Fee Input"):
            # Dynamically generate inputs based on the keys in the selected preset
            fees = {}
            for key in cost_fee_preset[selected_fee_preset].keys():
                # We use the key to get the display name and the default value for the input
                fees[key] = st.number_input(key, value=cost_fee_preset[selected_fee_preset][key])

        st.divider()

        st.markdown(
            """
            Web: [PropAlpha](https://www.prop-alpha.com/)  
            Twitter: [@PropAlphaTrades](https://twitter.com/PropAlphaTrades)  
            [![GitHub Repo](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/Prop-Alpha/PropAlphaEvalSolver/)
            """
        )

    # --- Computation Elements --- #
    if compute_button:
        # Reserve a spot for our status message
        status_message = st.empty()

        # Check if individual variables are defined and non-negative
        individual_vars_valid = all(
            [var is not None and var >= 0 for var in [win_pct, mfe, trades_per_day, stop_width, tp_width]])

        # Check if dictionaries are not empty and contain only non-negative values
        dict_values_non_negative = all([all(val >= 0 for val in d.values()) for d in [rules, fees]])

        # If all checks pass, perform the computation
        if individual_vars_valid and dict_values_non_negative and rules and fees:
            # Display a message saying the computation is running
            status_message.text("Computing... Please wait.")
            strategy = TradingStrategy(odds=win_pct, mfe=mfe, trades_per_day=trades_per_day,
                                       stop_width=stop_width, tp_width=tp_width)
            sim = Simulation(trading_strat=strategy, num_traders=int(monte_carlo_runs),
                             acct_rules=rules, acct_fees=fees)
            sim.run()
            result = sim.sim_results()
            status_message.text(result)
        else:
            st.warning("Please ensure all input values are provided and non-negative before computing.")


if __name__ == '__main__':
    run()
