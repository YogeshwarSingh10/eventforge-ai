import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "events.csv"


def load_events_dataset():
    return pd.read_csv(DATA_PATH)