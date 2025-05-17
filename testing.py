from misc_funs import *
data = load_json(USERS_FILE)
# Specify the CSV file name
csv_file = "USERS.csv"

# Extract the keys from the first dictionary to use as headers
headers = ["id"] + list(next(iter(data.values())).keys())

# Write the JSON data to a CSV file
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(headers)

    # Write the data rows
    for id, details in data.items():
        writer.writerow([id] + list(details.values()))

print(f"Data has been exported to {csv_file}")