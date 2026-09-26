import pandas as pd


file_path = "output/processed_features.csv"

df = pd.read_csv(file_path)


print("=" * 50)
print("STUDENT 1 PIPELINE VALIDATION")
print("=" * 50)


print(f"Rows: {len(df)}")

print(f"Columns: {len(df.columns)}")

print(
    f"Missing values: {df.isnull().sum().sum()}"
)


required_features = [

    "rms",

    "kurtosis",

    "crest_factor",

    "rms_z_score",

    "kurtosis_z_score"

]


print("\nRequired features:")


for feature in required_features:

    if feature in df.columns:

        print(f"[OK] {feature}")

    else:

        print(f"[MISSING] {feature}")


print("\nValidation completed.")