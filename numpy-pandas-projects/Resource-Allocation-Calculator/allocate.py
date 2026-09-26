import pandas as pd
from config import RATIOS

# lOAD PATIENT DATA
df = pd.read_csv("data/patients.csv")

# STANDARDIZE DEPARTMENT NAMES - lowercase, strip spaces
df["department"] = df["department"].str.lower().str.strip()