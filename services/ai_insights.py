class AIInsights:

    def __init__(self, df):
        self.df = df

    def generate_insights(self):
        if self.df.empty:
            return ["No data available yet."]

        insights = []

        income = self.df[self.df.type=="income"]["amount"].sum()
        expense = self.df[self.df.type=="expense"]["amount"].sum()

        # Savings check
        if expense > income * 0.8:
            insights.append("⚠️ Expenses are more than 80% of income. Savings risk detected.")
        elif expense < income * 0.5:
            insights.append("✅ Good savings rate. You are managing expenses well.")

        # Biggest category
        exp_df = self.df[self.df.type=="expense"]
        if not exp_df.empty:
            top_cat = exp_df.groupby("category")["amount"].sum().idxmax()
            top_amount = exp_df.groupby("category")["amount"].sum().max()
            insights.append(f"💸 Highest spending category: {top_cat} (₹ {top_amount:.0f})")

        # Monthly trend
        self.df["month"] = self.df["date"].str[:7]
        monthly = self.df.groupby(["month","type"])["amount"].sum().unstack(fill_value=0)

        if len(monthly) >= 2:
            last = monthly.iloc[-1].get("expense",0)
            prev = monthly.iloc[-2].get("expense",0)

            if last > prev:
                insights.append("📈 Your expenses increased compared to last month.")
            else:
                insights.append("📉 Good! Expenses decreased compared to last month.")

        # Budget suggestion
        if income > 0:
            recommended_budget = income * 0.6
            insights.append(f"🤖 Suggested monthly expense limit: ₹ {recommended_budget:.0f}")

        return insights
