import pandas as pd
from sklearn.linear_model import LinearRegression

from eventforge.tools.data_loader import load_events_dataset


class PricingModel:

    def __init__(self):
        self.model = LinearRegression()
        self._train()

    def _train(self):
        df = load_events_dataset()

        X = df[
            [
                "audience_size",
                "duration_days",
                "sponsors_count",
                "speakers_count",
            ]
        ]

        y = df["attendance"]

        self.model.fit(X, y)

    def predict_attendance(self, audience_size, duration, sponsors, speakers):
        X = [[audience_size, duration, sponsors, speakers]]
        return int(self.model.predict(X)[0])
    

def suggest_base_price(geography: str, audience_size: int) -> int:
    if "india" in geography.lower():
        return 40 if audience_size < 2000 else 60
    return 100