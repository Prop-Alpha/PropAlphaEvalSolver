# this is an adaptation of Vespatrades's work here:
# https://github.com/vespatrades/PropAlphaEvalCalculator_Streamlit/blob/master/streamlit_app.py

import streamlit as st
from simulation import Simulation
from trading_strategies import TradingStrategy


def run():
    
    st.markdown(
        '<a href="https://www.prop-alpha.com/" target="_blank">'
        '<img src="./app/static/propalpha_banner.png" width="700">'
        '</a>',
        unsafe_allow_html=True,
    )

    st.title("Prop Alpha Eval Solver")

    st.markdown("""
        Estimate the expected full payout value for prop trading accounts, given 
        costs, fees, rules, and a trade strategy. Factors in EOD trailing 
        drawdown. Strategy includes defined order bracket, win rate, and average MFE.\n
        NOT FINANCIAL ADVICE.\n
        DO YOUR OWN RESEARCH.\n
        NO GUARANTEE OUR MATH IS CORRECT.\n
        RISK DISCLAIMER: https://www.prop-alpha.com/disclaimer
    """)

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

    with st.container():
        with st.sidebar:
            st.subheader('Account Rules')

            selected_acct_preset = st.selectbox(label="Account", options=list(account_rule_presets.keys()))
            st.caption('Select Custom and use Advanced to enter custom values.')
            with st.expander("Advanced Account Rules"):
                intial_balance_eval = st.number_input("Initial Balance (Eval)",
                                            value=account_rule_presets[selected_acct_preset]["Initial Balance (Eval)"], step=100)

                initial_balance_funded = st.number_input("Initial Balance (Funded)",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Initial Balance (Funded)"], step=100)

                max_loss_eval = st.number_input("Max Loss (Eval)",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Max Loss (Eval)"], step=100)

                max_loss_funded = st.number_input("Max Loss (Funded)",
                                                value=account_rule_presets[selected_acct_preset][
                                                    "Max Loss (Funded)"], step=100)

                funding_target_balance = st.number_input("Funding Target Balance",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Funding Target Balance"], step=100)

                unshared_winning_balance_funded = st.number_input("Unshared Winning Balance (Funded)",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Unshared Winning Balance (Funded)"], step=100)

                profit_share_fraction = st.number_input("Profit Share Fraction",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Profit Share Fraction"], step=0.1)

                winning_day_pnl_min = st.number_input("Winning Day PnL Minimum",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Winning Day PnL Minimum"], step=100)

                max_daily_loss = st.number_input("Maximum Daily Loss",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Maximum Daily Loss"], step=100)

                max_daily_win = st.number_input("Maximum Daily Win",
                                                      value=account_rule_presets[selected_acct_preset][
                                                          "Maximum Daily Win"], step=100)

                min_winning_days_for_payout = st.number_input("Minimum Winning Days for Payout",
                                                value=account_rule_presets[selected_acct_preset][
                                                    "Minimum Winning Days for Payout"], step=1)

                minimum_winning_balance = st.number_input("Minimum Winning Balance",
                                                              value=account_rule_presets[selected_acct_preset][
                                                                  "Minimum Winning Balance"], step=100)

            rules = {
                'Initial Balance (Eval)': intial_balance_eval,
                'Initial Balance (Funded)': initial_balance_funded,
                'Max Loss (Eval)': max_loss_eval,
                'Max Loss (Funded)': max_loss_funded,
                'Funding Target Balance': funding_target_balance,
                'Unshared Winning Balance (Funded)': unshared_winning_balance_funded,
                'Profit Share Fraction': profit_share_fraction,
                'Winning Day PnL Minimum': winning_day_pnl_min,
                'Maximum Daily Loss': max_daily_loss,
                'Maximum Daily Win': max_daily_win,
                'Minimum Winning Days for Payout': min_winning_days_for_payout,
                'Minimum Winning Balance': minimum_winning_balance
            }

            st.divider()
            st.subheader('Account Costs/Fees')
            selected_fee_preset = st.selectbox(label="Costs/fees", options=list(cost_fee_preset.keys()))
            st.caption('Select Custom and use Advanced to enter custom values.')

            with st.expander("Advanced Cost/Fee Inputs"):
                # Cost/fee
                eval_cost = st.number_input("Eval Account Cost",
                                            value=cost_fee_preset[selected_fee_preset]["Eval Acct Cost"], step=1)

                funded_cost = st.number_input("Funded Account Setup Cost",
                                              value=cost_fee_preset[selected_fee_preset]["Funded Acct Setup Cost"], step=1)

                per_side_cost = st.number_input("Per Side Trade Cost",
                                                value=cost_fee_preset[selected_fee_preset]["Per Side Trade Cost"])

                trade_entry_slippage = st.number_input("Trade Entry Slippage Estimate in Currency",
                                                       value=cost_fee_preset[selected_fee_preset]["Trade Entry Slippage"])

                trade_stop_slippage = st.number_input("Stop Loss Slippage Estimate in Currency",
                                                      value=cost_fee_preset[selected_fee_preset]["Trade Stop Slippage"])

                monthly_cost = st.number_input("Monthly Funded Account Cost",
                                               value=cost_fee_preset[selected_fee_preset]["Monthly Funded Account Cost"])
            fees = {
                "Eval Acct Cost": eval_cost,
                "Funded Acct Setup Cost": funded_cost,
                "Per Side Trade Cost": per_side_cost,
                "Trade Entry Slippage": trade_entry_slippage,
                "Trade Stop Slippage": trade_stop_slippage,
                "Monthly Funded Account Cost": monthly_cost
            }

            st.divider()

            st.markdown(
                """
                Web: [PropAlpha](https://www.prop-alpha.com/)
                
                Twitter: [@PropAlphaTrades](https://twitter.com/PropAlphaTrades)
                """
            )

        st.divider()
        st.subheader('Trade Strategy')
        stop_width = st.number_input(label="Enter Stop Size in Currency", help="Stop loss in dollars", value=3000,
                                     step=100)

        tp_width = st.number_input(label="Enter Take Profit Size in Currency", help="Take profit in dollars",
                                   value=3000, step=100)

        win_pct = st.number_input(label="Enter Estimated Win Percent", help="", value=50.0, step=0.1)
        win_pct /= 100 # convert the percentage value into a proportion

        mfe = st.number_input(label="Enter Estimated MFE (of Losing Trades) in Currency", value=500, step=10)

        trades_per_day = st.number_input(label="Enter Number of Trades Per Day",
                                         help="Number of trades strategy takes in a single day", value=3, step=1)

        monte_carlo_runs = st.number_input("Enter Number of Runs in Simulation", value=20000, step=1000)

    compute_button = st.button("Compute Results")

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
                             acct_rules=rules, acct_fees=fees)
            sim.run()
            result = sim.sim_results()
            status_message.text(result)
        else:
            st.warning("Please provide all input values before computing.")


if __name__ == '__main__':
    run()
