import pandas as pd
from datetime import datetime
import os

def save_data(emotion, attention):
    file = "data.csv"

    data = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Emotion": emotion,
        "Attention": attention
    }

    df = pd.DataFrame([data])

    if not os.path.exists(file):
        df.to_csv(file, index=False)
    else:
        df.to_csv(file, mode='a', header=False, index=False)