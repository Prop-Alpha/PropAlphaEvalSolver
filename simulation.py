import numpy as np
from trader import Trader
from io import BytesIO
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, trading_strat, num_traders, acct_rules, acct_fees):
        self.min_winning_trader_number = None
        self.max_winning_trader_number = None
        self.winning_trader_numbers = []
        self.strategy = trading_strat
        self.num_traders = num_traders
        trader_array = [Trader(self.strategy, acct_rules=acct_rules, acct_fees=acct_fees) for i in range(num_traders)]
        self.traders = {i: j for (i, j) in zip(range(num_traders), trader_array)}
        self.avg_pnl = 0
        self.avg_days = 0
        self.avg_days_to_win = 0
        self.avg_days_to_lose = 0
        self.pct_wins = 0
        self.avg_win_pnl = 0
        self.avg_lose_pnl = 0
        self.pct_pass_eval = 0
        self.max_payout = 0
        self.min_payout = float('inf')
        self.max_days_to_win = 0
        self.min_days_to_win = float('inf')
        self.max_days_to_lose = 0
        self.min_days_to_lose = float('inf')

    def run(self):
        # simulate trading for all traders
        sum_pnl = 0
        sum_days = 0
        sum_win_days = 0
        sum_loss_days = 0
        sum_winning_traders = 0
        sum_losing_traders = 0
        sum_winning_pnl = 0
        sum_losing_pnl = 0
        sum_passed_eval = 0

        # TODO: parallelize to run this part on multiple cores
        for trader_num in range(len(self.traders)):
            while not (self.traders[trader_num].account.won or self.traders[trader_num].account.failed):
                self.traders[trader_num].trade_for_day()
                if self.traders[trader_num].account.total_days > 700:
                    print(f"traded too damn long with no win, acct balance: {self.traders[trader_num].account.balance}")
                    print(f'winning days: {self.traders[trader_num].account.winning_days}')
                    break
            sum_days += self.traders[trader_num].account.total_days
            sum_pnl += self.traders[trader_num].PnL
            if not self.traders[trader_num].account.in_eval:
                sum_passed_eval += 1
            if self.traders[trader_num].account.won:
                self.winning_trader_numbers.append(trader_num)
                sum_winning_traders += 1
                sum_win_days += self.traders[trader_num].account.total_days
                sum_winning_pnl += self.traders[trader_num].PnL
                if self.traders[trader_num].account.total_days < self.min_days_to_win:
                    self.min_days_to_win = self.traders[trader_num].account.total_days
                if self.traders[trader_num].account.total_days > self.max_days_to_win:
                    self.max_days_to_win = self.traders[trader_num].account.total_days
                if self.traders[trader_num].PnL < self.min_payout:
                    self.min_payout = self.traders[trader_num].PnL
                    self.min_winning_trader_number = trader_num
                if self.traders[trader_num].PnL > self.max_payout:
                    self.max_payout = self.traders[trader_num].PnL
                    self.max_winning_trader_number = trader_num

            elif self.traders[trader_num].account.failed:
                if self.traders[trader_num].account.total_days < self.min_days_to_lose:
                    self.min_days_to_lose = self.traders[trader_num].account.total_days
                if self.traders[trader_num].account.total_days > self.max_days_to_lose:
                    self.max_days_to_lose = self.traders[trader_num].account.total_days
                sum_losing_traders += 1
                sum_loss_days += self.traders[trader_num].account.total_days
                sum_losing_pnl += self.traders[trader_num].PnL

        self.avg_pnl = sum_pnl / len(self.traders)
        self.avg_days = sum_days / len(self.traders)
        if sum_winning_traders > 0:
            self.avg_days_to_win = sum_win_days / sum_winning_traders
            self.avg_win_pnl = sum_winning_pnl / sum_winning_traders
        else:
            self.avg_days_to_win = 0
            self.avg_win_pnl = 0
        if sum_losing_traders > 0:
            self.avg_days_to_lose = sum_loss_days / sum_losing_traders
            self.avg_lose_pnl = sum_losing_pnl / sum_losing_traders
        else:
            self.avg_days_to_lose = 0
            self.avg_lose_pnl = 0
        self.pct_wins = (sum_winning_traders / len(self.traders)) * 100
        self.pct_pass_eval = (sum_passed_eval / len(self.traders)) * 100

    def run_eval_only(self):
        # simulate trading for all traders
        sum_days = 0
        sum_win_days = 0
        sum_loss_days = 0
        sum_winning_traders = 0
        sum_losing_traders = 0
        sum_passed_eval = 0

        for trader_num in range(len(self.traders)):
            while not self.traders[trader_num].passed_eval and not self.traders[trader_num].account.failed:
                self.traders[trader_num].trade_for_day()
                if self.traders[trader_num].account.total_days > 700:
                    print(f"traded too damn long with no win, acct balance: {self.traders[trader_num].account.balance}")
                    print(f'winning days: {self.traders[trader_num].account.winning_days}')
                    break
            sum_days += self.traders[trader_num].account.total_days
            if not self.traders[trader_num].account.in_eval:
                sum_passed_eval += 1
                sum_win_days += self.traders[trader_num].account.total_days

            else:
                sum_losing_traders += 1
                sum_loss_days += self.traders[trader_num].account.total_days

        self.avg_days = sum_days / len(self.traders)
        if sum_passed_eval > 0:
            self.avg_days_to_win = sum_win_days / sum_passed_eval
        else:
            self.avg_days_to_win = 0
            self.avg_win_pnl = 0
        if sum_losing_traders > 0:
            self.avg_days_to_lose = sum_loss_days / sum_losing_traders
        else:
            self.avg_days_to_lose = 0
            self.avg_lose_pnl = 0
        self.pct_wins = (sum_winning_traders / len(self.traders)) * 100
        self.pct_pass_eval = (sum_passed_eval / len(self.traders)) * 100

    def run_funded_only(self):
        # simulate trading for all traders
        sum_pnl = 0
        sum_days = 0
        sum_win_days = 0
        sum_loss_days = 0
        sum_winning_traders = 0
        sum_losing_traders = 0
        sum_winning_pnl = 0
        sum_losing_pnl = 0

        # TODO: parallelize?
        for trader_num in range(len(self.traders)):
            self.traders[trader_num].account.passed_eval()
            while not (self.traders[trader_num].account.won or self.traders[trader_num].account.failed):
                self.traders[trader_num].trade_for_day()
                if self.traders[trader_num].account.total_days > 700:
                    print(f"traded too damn long with no win, acct balance: {self.traders[trader_num].account.balance}")
                    print(f'winning days: {self.traders[trader_num].account.winning_days}')
                    break
            sum_days += self.traders[trader_num].account.total_days
            sum_pnl += self.traders[trader_num].PnL
            if self.traders[trader_num].account.won:
                self.winning_trader_numbers.append(trader_num)
                sum_winning_traders += 1
                sum_win_days += self.traders[trader_num].account.total_days
                sum_winning_pnl += self.traders[trader_num].PnL
                if self.traders[trader_num].account.total_days < self.min_days_to_win:
                    self.min_days_to_win = self.traders[trader_num].account.total_days
                if self.traders[trader_num].account.total_days > self.max_days_to_win:
                    self.max_days_to_win = self.traders[trader_num].account.total_days
                if self.traders[trader_num].PnL < self.min_payout:
                    self.min_payout = self.traders[trader_num].PnL
                    self.min_winning_trader_number = trader_num
                if self.traders[trader_num].PnL > self.max_payout:
                    self.max_payout = self.traders[trader_num].PnL
                    self.max_winning_trader_number = trader_num

            elif self.traders[trader_num].account.failed:
                if self.traders[trader_num].account.total_days < self.min_days_to_lose:
                    self.min_days_to_lose = self.traders[trader_num].account.total_days
                if self.traders[trader_num].account.total_days > self.max_days_to_lose:
                    self.max_days_to_lose = self.traders[trader_num].account.total_days
                sum_losing_traders += 1
                sum_loss_days += self.traders[trader_num].account.total_days
                sum_losing_pnl += self.traders[trader_num].PnL

        self.avg_pnl = sum_pnl / len(self.traders)
        self.avg_days = sum_days / len(self.traders)
        if sum_winning_traders > 0:
            self.avg_days_to_win = sum_win_days / sum_winning_traders
            self.avg_win_pnl = sum_winning_pnl / sum_winning_traders
        else:
            self.avg_days_to_win = 0
            self.avg_win_pnl = 0
        if sum_losing_traders > 0:
            self.avg_days_to_lose = sum_loss_days / sum_losing_traders
            self.avg_lose_pnl = sum_losing_pnl / sum_losing_traders
        else:
            self.avg_days_to_lose = 0
            self.avg_lose_pnl = 0
        self.pct_wins = (sum_winning_traders / len(self.traders)) * 100

    def sim_results(self):
        return {
            "Estimated Subscription EV": f"${self.avg_pnl:.2f}",
            "Average Number of Days Traded": f"{self.avg_days:.1f}",
            "Percent Wins (Full Payout)": f"{self.pct_wins:.2f}%",
            "Average Days Traded On Winning Runs": f"{self.avg_days_to_win:.1f}",
            "Max Days Traded On Winning Run": self.max_days_to_win,
            "Min Days Traded On Winning Run": self.min_days_to_win,
            "Average Days Traded On Losing Runs": f"{self.avg_days_to_lose:.1f}",
            "Max Days Traded On Losing Run": self.max_days_to_lose,
            "Min Days Traded On Losing Run": self.min_days_to_lose,
            "Average Winning Payout": f"${self.avg_win_pnl:.2f}",
            "Max Winning Payout": f"${self.max_payout:.2f}",
            "Min Winning Payout": f"${self.min_payout:.2f}",
            "Average Loss Cost": f"${self.avg_lose_pnl:.2f}",
            "Percent Pass Eval": f"{self.pct_pass_eval:.2f}%"
        }

    def eval_only_sim_results(self):
        return {
            "Average Number of Days Traded": f"{self.avg_days:.1f}",
            "Average Days Traded On Winning Runs": f"{self.avg_days_to_win:.1f}",
            "Average Days Traded On Losing Runs": f"{self.avg_days_to_lose:.1f}",
            "Percent Pass Combine": f"{self.pct_pass_eval:.2f}%"
        }

    def funded_only_sim_results(self):
        return {
            "Estimated Account EV": f"${self.avg_pnl:.2f}",
            "Average Number of Days Traded": f"{self.avg_days:.1f}",
            "Percent Wins (Full Payout)": f"{self.pct_wins:.2f}%"
        }

    def plot_outcomes(self):
        # Store the equity curve for this simulation along with its color
        # Plot each equity curve with the computed y-axis limits
        # Compute y-axis limits for the plots

        plt.figure(figsize=(12, 8))  # Set the figure size to 8 inches wide and 6 inches tall
        final_winning_balances = [self.traders[i].running_balance[-1] for i in self.winning_trader_numbers]
        median_final_balance = np.median(np.array(final_winning_balances))
        median_balance_number = None
        for i in self.winning_trader_numbers:
            if self.traders[i].running_balance[-1] == median_final_balance:
                median_balance_number = i
        max_winning_trader = self.traders[self.max_winning_trader_number]
        min_winning_trader = self.traders[self.min_winning_trader_number]
        plt.plot(max_winning_trader.running_balance, color='blue', label='max payout')
        if median_balance_number:
            plt.plot(self.traders[median_balance_number].running_balance, color='black', label='median payout')
        plt.plot(min_winning_trader.running_balance, color='red', label='min payout')
        min_value = min(min(max_winning_trader.running_balance), min(min_winning_trader.running_balance))
        max_value = max(max(max_winning_trader.running_balance), max(min_winning_trader.running_balance))
        plt.ylim(min_value, max_value)
        plt.xlabel('Number of Days Traded')
        plt.ylabel('Account Balance')
        plt.title('Topstep 150k Account Simulation')
        plt.legend(loc='upper right')
        # plt.show()  # display the plot once after all curves have been plotted
        # TODO: hockey stick plot, histogram (condition on win?)
        buf = BytesIO()  # Create a bytes buffer to save the image
        plt.savefig(buf, format="png")  # Save the image to the buffer
        plt.close()  # Close the plot

        buf.seek(0)  # Move the cursor to the start of the buffer
        return buf  # Return the buffer containing the image data

