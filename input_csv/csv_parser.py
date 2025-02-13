import csv
import re

def extract_street_and_house(address):
    # Use regex to split street name and house number
    match = re.match(r"(.+?)\s+(\d+[\w\-/]*)$", address)
    if match:
        return match.group(1), match.group(2)  # Street name, house number
    return address, ""  # If no match, return full address as street name, empty house number

def filter_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        writer.writerow(["pincode", "street_name", "house_number"])
        
        for row in reader:
            if len(row) >= 5:  # Ensure row has enough columns
                pincode = row[3].strip()
                street, house_no = extract_street_and_house(row[4].strip())
                writer.writerow([pincode, street, house_no])

# Example usage
filter_csv("Adresses_for_crawler.csv", "filtered_adress.csv")
