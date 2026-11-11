
import pandas as pd

# Step 1: Load raw dataset
df = pd.read_csv("data/raw_dataset.csv")

print("RAW DATASET")
print(df)

# Step 2: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Step 3: Handle missing household consumption
consumption_median = df["household_consumption_kwh"].median()

df["household_consumption_kwh"] = (
    df["household_consumption_kwh"].fillna(consumption_median)
)

# Step 4: Handle invalid negative solar readings
valid_solar = df.loc[
    df["solar_generation_kwh"] >= 0,
    "solar_generation_kwh"
]

solar_median = valid_solar.median()

df.loc[
    df["solar_generation_kwh"] < 0,
    "solar_generation_kwh"
] = solar_median

# Step 5: Round energy readings
df["household_consumption_kwh"] = (
    df["household_consumption_kwh"].round(2)
)

df["solar_generation_kwh"] = (
    df["solar_generation_kwh"].round(2)
)

# Step 6: Save cleaned dataset
df.to_csv("data/cleaned_dataset.csv", index=False)

print("\nCLEANED DATASET")
print(df)

print("\nCleaned dataset saved successfully!")
