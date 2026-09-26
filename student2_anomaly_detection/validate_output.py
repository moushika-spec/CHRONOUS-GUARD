# type:ignore 
import pandas as pd

from config import OUTPUT_FILE

df = pd.read_csv(OUTPUT_FILE)

print("=" * 50)

print("STUDENT 2 VALIDATION")

print("=" * 50)

print(f"Rows : {len(df)}")

print(f"Columns : {len(df.columns)}")

print(f"Missing Values : {df.isnull().sum().sum()}")

required = [

    "prediction",

    "anomaly_score",

    "health_index",

    "remaining_useful_life"

]

print()

for col in required:

    if col in df.columns:

        print(f"[OK] {col}")

    else:

        print(f"[MISSING] {col}")

print("\nValidation Successful.")