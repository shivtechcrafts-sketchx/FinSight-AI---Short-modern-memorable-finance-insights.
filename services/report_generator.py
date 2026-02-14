import os

class ReportGenerator:
    def __init__(self, analytics):
        self.analytics = analytics
        os.makedirs("result", exist_ok=True)

    def export_csv(self):
        df = self.analytics.load_dataframe()
        df.to_csv("result/report.csv", index=False)
