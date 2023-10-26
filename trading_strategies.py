import numpy as np
# import matplotlib.pyplot as plt


class TradingStrategy:
    def __init__(self, odds, mfe, trades_per_day, stop_width, tp_width):
        self.odds = odds  # probability of success
        self.mfe = mfe  # in currency
        self.trades_per_day = trades_per_day
        # TODO: randomize trades per day?
        self.bracket_stop_width_currency = stop_width
        self.bracket_tp_width_currency = tp_width

    def simulate_return(self, per_side_cost=0, entry_slippage=0, stop_slippage=0):
        # Simulate the return for a single trade using the strategy stats
        return np.random.choice([self.bracket_tp_width_currency - per_side_cost - entry_slippage,
                                 -self.bracket_stop_width_currency - per_side_cost - entry_slippage - stop_slippage],
                                p=[self.odds, 1 - self.odds])

    def simulate_favorable_excursion(self):
        if self.mfe * 2 <= self.bracket_tp_width_currency:
            return np.random.uniform(0, 2 * self.mfe)
        else:
            tp_minus_mfe = self.bracket_tp_width_currency - self.mfe
            if tp_minus_mfe > 0:
                return np.random.uniform(self.mfe - tp_minus_mfe, self.bracket_tp_width_currency)
            else:
                return self.mfe
