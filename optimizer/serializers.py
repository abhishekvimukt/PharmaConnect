from rest_framework import serializers
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import MR, Doctor, OutcomeCode, PlantoMR, VisitRes, Achievement, Challenge, Expense, Medicine, Voice_assist
from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError

class UserCreateSerializer(BaseUserCreateSerializer):
    mr_id = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    region = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'mr_id', 'name', 'phone', 'region']

    def validate(self, attrs):
        # Remove MR fields before validation
        mr_fields = ['mr_id', 'name', 'phone', 'region']
        user_data = {key: attrs[key] for key in attrs if key not in mr_fields}
        
        # Validate user data
        user = User(**user_data)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            # Extract MR specific data
            mr_data = {
                'mr_id': validated_data.pop('mr_id'),
                'name': validated_data.pop('name'),
                'phone': validated_data.pop('phone'),
                'region': validated_data.pop('region'),
                'email': validated_data.get('email', '')
            }
            
            # Create user
            user = User.objects.create_user(**validated_data)
            
            # Create MR profile
            MR.objects.create(user=user, **mr_data)
            
            return user
        except IntegrityError:
            self.fail("cannot_create_user")

class UserSerializer(BaseUserSerializer):
    mr_profile = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mr_profile']

    def get_mr_profile(self, obj):
        if hasattr(obj, 'mr_profile'):
            return {
                'mr_id': obj.mr_profile.mr_id,
                'name': obj.mr_profile.name,
                'phone': obj.mr_profile.phone,
                'email': obj.mr_profile.email,
                'region': obj.mr_profile.region,
                'is_active': obj.mr_profile.is_active
            }
        return None

class MRSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = MR
        fields = ['mr_id', 'name', 'phone', 'email', 'region', 'is_active', 'user_details']

    def get_user_details(self, obj):
        if obj.user:
            return {
                'username': obj.user.username,
                'email': obj.user.email,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name
            }
        return None

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class OutcomeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCode
        fields = '__all__'

class PlantoMRSerializer(serializers.ModelSerializer):
    mr = MRSerializer(read_only=True)
    mr_id = serializers.PrimaryKeyRelatedField(queryset=MR.objects.all(), source='mr', write_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)
    class Meta:
        model = PlantoMR
        fields = '__all__'

class VisitResSerializer(serializers.ModelSerializer):
    mr = MRSerializer(read_only=True)
    mr_id = serializers.PrimaryKeyRelatedField(queryset=MR.objects.all(), source='mr', write_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)
    outcome_code = OutcomeCodeSerializer(read_only=True)
    outcome_code_id = serializers.PrimaryKeyRelatedField(queryset=OutcomeCode.objects.all(), source='outcome_code', write_only=True)
    class Meta:
        model = VisitRes
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    mr = MRSerializer(read_only=True)
    mr_id = serializers.PrimaryKeyRelatedField(queryset=MR.objects.all(), source='mr', write_only=True)
    class Meta:
        model = Achievement
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    mr = MRSerializer(read_only=True)
    mr_id = serializers.PrimaryKeyRelatedField(queryset=MR.objects.all(), source='mr', write_only=True)
    class Meta:
        model = Challenge
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    mr = MRSerializer(read_only=True)
    mr_id = serializers.PrimaryKeyRelatedField(queryset=MR.objects.all(), source='mr', write_only=True)
    class Meta:
        model = Expense
        fields = '__all__'
        
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        
class Voice_assistSerializer(serializers.ModelSerializer):
    class Meta:
        model= Voice_assist
        fields= '__all__'