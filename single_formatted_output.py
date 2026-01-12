import pandas as pd
import os

# Read CSV files (Windows paths fixed)
f1 = pd.read_csv("C:/Users/0wner/Downloads/GIT_Folder/quantium-starter-repo-main/data/daily_sales_Data_0.csv")
f2 = pd.read_csv("C:/Users/0wner/Downloads/GIT_Folder/quantium-starter-repo-main/data/daily_sales_Data_1.csv")
f3 = pd.read_csv("C:/Users/0wner/Downloads/GIT_Folder/quantium-starter-repo-main/data/daily_sales_Data_2.csv")

# Combine files
df = pd.concat([f1, f2, f3])

# Oly Pink Morsels
df = df[df["product"] == "Pink Morsels"]

# Create Sales column
df["Sales"] = df["quantity"] * df["price"]

# Keep only needed columns
df = df[["Sales", "date", "region"]]

# Rename columns
df.columns = ["Sales", "Date", "Region"]

# Make sure output folder exists
if not os.path.exists("output"):
    os.makedirs("output")

# Save final CSV
df.to_csv("output/pink_morsels_sales.csv", index=False)
