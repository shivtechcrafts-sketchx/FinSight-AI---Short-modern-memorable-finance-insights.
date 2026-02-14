import pandas as pd

class Analytics:
    def __init__(self, db):
        self.db = db

    def load_dataframe(self):
        return pd.read_sql_query("SELECT * FROM transactions", self.db.conn)

    def summary(self):
        df = self.load_dataframe()
        income = df[df.type=="income"]["amount"].sum()
        expense = df[df.type=="expense"]["amount"].sum()
        savings = income - expense
        return income, expense, savings
