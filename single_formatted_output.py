import csv
import os

DATA_DIRECTORY = "./data"
OUTPUT_FILE_PATH = "./formatted_data.csv"

# Step 1: Gather all rows for Pink Morsels
pink_morsels_rows = []

# Step 2: Loop over each CSV file in the data directory
for file_name in os.listdir(DATA_DIRECTORY):
    file_path = os.path.join(DATA_DIRECTORY, file_name)
    with open(file_path, mode="r", newline="") as input_file:
        reader = csv.DictReader(input_file)  # Use DictReader for clarity
        # Step 3: Loop through each row in the file
        for row in reader:
            if row["product"].lower() == "pink morsel":
                # Calculate sale
                price = float(row["price"].lstrip("$"))
                quantity = int(row["quantity"])
                sale = price * quantity

                # Add the formatted row to our list
                pink_morsels_rows.append({
                    "sales": sale,
                    "date": row["date"],
                    "region": row["region"]
                })

# Step 4: Write all collected rows to the output CSV
with open(OUTPUT_FILE_PATH, mode="w", newline="") as output_file:
    fieldnames = ["sales", "date", "region"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in pink_morsels_rows:
        writer.writerow(row)

print("Formatted CSV created successfully!")
