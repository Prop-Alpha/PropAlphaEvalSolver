class TopstepAccount:

    def __init__(self, acct_rules):
        self.rules = acct_rules

        self.in_eval = True
        self.balance = acct_rules['Initial Balance (Eval)']
        self.minimum_balance = self.balance - acct_rules['Max Loss (Eval)']
        self.failed = False
        self.winning_days = 0
        self.daily_pnl = 0
        self.eval_hwm = self.balance
        self.won = False
        self.total_days = 0

    def funded_full_payout(self):
        return (self.balance - self.rules['Unshared Winning Balance (Funded)']) * self.rules['Profit Share Fraction'] \
            + (self.rules['Unshared Winning Balance (Funded)'] - self.rules['Initial Balance (Funded)'])

    def passed_eval(self):
        self.in_eval = False
        self.balance = self.rules['Initial Balance (Funded)']
        self.minimum_balance = self.balance - self.rules['Max Loss (Funded)']

    def new_day(self):
        self.daily_pnl = 0

    def end_of_day_update(self):
        self.total_days += 1
        if self.in_eval:
            if self.balance > self.eval_hwm:
                self.minimum_balance += self.balance - self.eval_hwm
                self.eval_hwm = self.balance
        else:
            if self.daily_pnl > 0 and self.minimum_balance < self.rules['Initial Balance (Funded)']:
                self.minimum_balance = min(self.minimum_balance + self.daily_pnl,
                                           self.rules['Initial Balance (Funded)'])
            if self.daily_pnl >= self.rules['Winning Day PnL Minimum']:
                self.winning_days += 1

        self.new_day()

    def trade(self, trade_return, mfe=0):

        if self.in_eval and trade_return < 0:
            if self.balance + mfe >= self.rules['Funding Target Balance']:
                self.end_of_day_update()
                self.passed_eval()
                return 'PASS EVAL'
            if self.daily_pnl + mfe >= self.rules['Maximum Daily Win']:
                new_trade_return = self.rules['Maximum Daily Win'] - self.daily_pnl
                self.balance += new_trade_return
                self.daily_pnl = self.rules['Maximum Daily Win']
                self.end_of_day_update()
                return 'DAILY WIN STOP'

        self.daily_pnl += trade_return

        self.balance += trade_return

        if self.in_eval and self.balance >= self.rules['Funding Target Balance']:
            self.end_of_day_update()
            self.passed_eval()
            return 'PASS EVAL'

        if self.balance <= self.minimum_balance:
            self.failed = True
            return 'FAIL'

        if self.daily_pnl <= -self.rules['Maximum Daily Loss']:
            self.end_of_day_update()
            return 'DAILY LOSS LIMIT STOP'

        # TODO: dont take trades if TP would cross max daily win limit (option)

        if self.in_eval and self.daily_pnl >= self.rules['Maximum Daily Win']:
            self.daily_pnl -= trade_return
            self.balance -= trade_return
            new_trade_return = self.rules['Maximum Daily Win'] - self.daily_pnl
            self.balance += new_trade_return
            self.daily_pnl = self.rules['Maximum Daily Win']
            self.end_of_day_update()
            return 'DAILY WIN STOP'

        if self.daily_pnl >= self.rules['Winning Day PnL Minimum']:
            if self.winning_days >= self.rules['Minimum Winning Days for Payout'] - 1 \
                    and self.balance >= self.rules['Minimum Winning Balance']:
                self.won = True
                self.end_of_day_update()
                return 'SUCCEED'

        return 'NO DAILY OR TOTAL STOP CONDITION HIT'
