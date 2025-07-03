import os
import django

# STEP 1: Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr_optimizer_db.settings')
django.setup()

# STEP 2: Now import models
import openpyxl
from optimizer.models import Achievement

# STEP 3: Load workbook
wb = openpyxl.load_workbook("ColorCoded_MR_Report.xlsx")
sheet = wb["Achievements"]

# STEP 4: Loop and insert data
for row in sheet.iter_rows(min_row=2, values_only=True):
    if not row[0]:
        continue
    
    try:
        value_str = str(row[4]).replace('₹', '').replace(',', '').strip()
        est_value = float(value_str) if value_str.replace('.', '', 1).isdigit() else 0
    except Exception:
        est_value = 0

    Achievement.objects.create(
        type=row[0],
        product=row[1],
        details=row[2],
        quantity=int(row[3] or 0),
        est_value=est_value,
        # voice_input=row[5] or '',
        impact_score=int(row[6] or 0),
    )



print("✅ Data import complete.")
