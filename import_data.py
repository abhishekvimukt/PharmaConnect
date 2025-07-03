import csv
from optimizer.models import MR, Doctor, VisitPlan, VisitItem
from datetime import datetime
from django.utils.timezone import now

csv_file_path = 'synthetic_mr_doc.csv'

with open(csv_file_path, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        mr_id = row['MR_id']
        mr, _ = MR.objects.update_or_create(
            mr_id=mr_id,
            defaults={
                'name': f"MR {mr_id}",
                'phone': '',
                'email': f"{mr_id.lower()}@dummy.com",  # avoid duplicate ''
                'region': '',
            }
        )

        doctor, _ = Doctor.objects.update_or_create(
            doctor_id=row['doctor_id'],
            defaults={
                'name': row['doctor_name'],
                'specialization': row['specialization'],
                'location_lat': row['location_lat'],
                'location_long': row['location_lon'],
                'available_from': row['available_from'] or None,
                'available_to': row['available_to'] or None,
                'visit_duration_mins': int(row['visit_duration_mins'] or 0),
                'priority_score': float(row['priority_score'] or 0),
                'mr': mr,
                'others': row['others'],
            }
        )

        # Create VisitPlan
        visit_plan, _ = VisitPlan.objects.get_or_create(
            mr=mr,
            date=now().date(),  # dummy date
            defaults={'created_at': now()}
        )

        # Create VisitItem
        VisitItem.objects.update_or_create(
            visit_plan=visit_plan,
            doctor=doctor,
            defaults={
                'visit_order': 0,
                'scheduled_time': None
            }
        )
