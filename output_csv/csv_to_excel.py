import pandas as pd

def convert_csv_to_excel(csv_file, excel_file):
    # Read the CSV file with UTF-8 encoding to preserve special characters
    df = pd.read_csv(csv_file, encoding="utf-8")

    # Save to Excel while ensuring special characters are preserved
    df.to_excel(excel_file, index=False, engine="openpyxl")

    print(f"Successfully converted '{csv_file}' to '{excel_file}' while preserving special characters.")

# Example usage
convert_csv_to_excel("filtered_adress_results_f24.csv", "filtered_adress_results_f24.xlsx")

