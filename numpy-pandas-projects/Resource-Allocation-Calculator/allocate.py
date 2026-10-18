import pandas as pd
from config import RATIOS

# lOAD PATIENT DATA
df = pd.read_csv("data/patients.csv")



# STANDARDIZE DEPARTMENT NAMES - lowercase, strip spaces
df["department"] = df["department"].str.lower().str.strip()

# Check for unknown departments
known = set(RATIOS.keys())
incoming = set(df["department"])
unknown = incoming - known

if unknown:
    print(f"Warning: unknown departments found: {unknown}")
    df = df[df["department"].isin(known)]       # drop unknowns, keep going


# Calculate the required staff per department
results = []

for _, row in df.iterrows():
    dept = row["department"]
    patients = row["patient_count"]

    nurses_ratio = RATIOS[dept]["nurses"]
    doctors_ratio = RATIOS[dept]["doctors"]

    nurses_needed = -(-patients // nurses_ratio)    # ceiling division
    doctors_needed = -(-patients // doctors_ratio)

    results.append({
        "department": dept,
        "patient_count": patients,
        "nurses_needed": nurses_needed,
        "doctors_needed": doctors_needed
    })

results_df = pd.DataFrame(results)
print(results_df)