import pandas as pd
import json

df = pd.read_excel("medicine_catalog.xlsx")  # Adjust filename if needed

def build_entry(row, idx):
    return {
        "id": idx,
        "text": f"{row['product_name']} contains {row['composition']}. It is used for {row['usage']}. Precautions: {row['precautions']}. MRP: ₹{row['mrp']}. Manufacturer: {row['manufacturer']}."
    }

entries = [build_entry(row, idx) for idx, row in df.iterrows()]

with open("catalog_ai/medicine_data.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print("✅ JSON file saved to catalog_ai/medicine_data.json")
