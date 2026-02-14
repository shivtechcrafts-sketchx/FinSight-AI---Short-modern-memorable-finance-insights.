from datetime import datetime

class Transaction:
    def __init__(self, user_id, amount, category, t_type):
        self.user_id = user_id
        self.amount = float(amount)
        self.category = category
        self.type = t_type
        self.date = datetime.now().strftime("%Y-%m-%d")
