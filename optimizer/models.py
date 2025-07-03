from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings

class MR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mr_profile', null=True, blank=True)
    mr_id = models.CharField(max_length=10, db_column='MR_id', unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.mr_id})"

    class Meta:
        verbose_name = "Medical Representative"
        verbose_name_plural = "Medical Representatives"

class Doctor(models.Model):
    doctor_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default="Unknown")
    location = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.name

class OutcomeCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    meaning = models.CharField(max_length=100)
    mr_voice_equivalent = models.TextField()

    def __str__(self):
        return self.code

class PlantoMR(models.Model):
    plan_id = models.AutoField(primary_key=True)
    mr = models.ForeignKey(MR, on_delete=models.CASCADE, null=True, blank=True)  # Assigned MR, nullable for migration
    time = models.TimeField(null=True, blank=True)  # nullable for migration
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    product = models.CharField(max_length=100, null=True, blank=True)
    voice_input = models.TextField(models.ForeignKey,null=True, blank=True)
    auto_suggested = models.BooleanField(default=False)

    def __str__(self):
        return f"Plan {self.plan_id} for {self.doctor.name if self.doctor else 'Unknown'} by {self.mr.name if self.mr else 'Unassigned'}"

    class Meta:
        db_table = 'optimizer_plantoMR'

class VisitRes(models.Model):
    visit_id = models.AutoField(primary_key=True)
    mr = models.ForeignKey(MR, on_delete=models.CASCADE, null=True, blank=True)  # MR who did the visit, nullable for migration
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    visit_type = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=100, null=True, blank=True)
    outcome_code = models.ForeignKey(OutcomeCode, on_delete=models.SET_NULL, null=True, blank=True)
    key_insight = models.TextField(null=True, blank=True)
    ai_interpretation = models.TextField(null=True, blank=True)
    follow_up = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], null=True, blank=True)
    next_step = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)  # nullable for migration
    # doctor_id = models.CharField(max_length=10, foreign_key=Doctor.doctor_id)
    def __str__(self):
        return f"Visit {self.visit_id} to {self.doctor.name if self.doctor else 'Unknown'} by {self.mr.name if self.mr else 'Unassigned'}"

    class Meta:
        db_table = 'optimizer_visitRes'

class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    mr = models.ForeignKey(MR, on_delete=models.CASCADE, null=True, blank=True)  # MR who achieved, nullable for migration
    type = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    est_value = models.CharField(max_length=50, null=True, blank=True)
    voice_input = models.TextField(models.ForeignKey,null=True, blank=True)
    impact_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Achievement {self.achievement_id} by {self.mr.name if self.mr else 'Unassigned'}"

class Challenge(models.Model):
    challenge_id = models.AutoField(primary_key=True)
    mr = models.ForeignKey(MR, on_delete=models.CASCADE, null=True, blank=True)  # MR who faced the challenge, nullable for migration
    doctor_id = models.CharField(max_length=20, null=True, blank=True)  # Document ID for the challenge
    category = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    urgency = models.CharField(max_length=20, null=True, blank=True)
    voice_input = models.TextField(models.ForeignKey,null=True, blank=True)
    ai_suggested_action = models.TextField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Challenge {self.challenge_id} for {self.mr.name if self.mr else 'Unassigned'}"

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    mr = models.ForeignKey(MR, on_delete=models.CASCADE, null=True, blank=True)  # MR who logged the expense, nullable for migration
    category = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    voice_input = models.TextField(models.ForeignKey,null=True, blank=True)
    reimbursement_pending = models.BooleanField(default=True)

    def __str__(self):
        return f"Expense {self.expense_id} - {self.amount} for {self.mr.name if self.mr else 'Unassigned'}"

class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
 
 
#  voice_assist model just for voice input not an assistant 
class Voice_assist(models.Model):  
    voice_input = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Voice Assist: {str(self.voice_input)[:20]}" if self.voice_input else "Voice Assist Entry"
