from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import MR, Doctor, OutcomeCode, PlantoMR, VisitRes, Achievement, Challenge, Expense, Medicine, Voice_assist, User
from .serializers import (
    MRSerializer, DoctorSerializer, OutcomeCodeSerializer,
    PlantoMRSerializer, VisitResSerializer, AchievementSerializer,
    ChallengeSerializer, ExpenseSerializer, MedicineSerializer, Voice_assistSerializer,
    UserSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum,Avg

class IsMRUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'mr_profile'))

class MRViewSet(viewsets.ModelViewSet):
    queryset = MR.objects.all()
    serializer_class = MRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MR.objects.all()
        return MR.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def my_profile(self, request):
        try:
            mr = request.user.mr_profile
            serializer = self.get_serializer(mr)
            return Response(serializer.data)
        except MR.DoesNotExist:
            return Response(
                {"detail": "MR profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'])
    def my_plans(self, request):
        try:
            mr = request.user.mr_profile
            plans = PlantoMR.objects.filter(mr=mr)
            serializer = PlantoMRSerializer(plans, many=True)
            return Response(serializer.data)
        except MR.DoesNotExist:
            return Response(
                {"detail": "MR profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'])
    def my_visits(self, request):
        try:
            mr = request.user.mr_profile
            visits = VisitRes.objects.filter(mr=mr)
            serializer = VisitResSerializer(visits, many=True)
            return Response(serializer.data)
        except MR.DoesNotExist:
            return Response(
                {"detail": "MR profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='dashboard/manager')
    def manager_dashboard(self, request):
        total_mrs = MR.objects.count()
        # Example logic: active MRs are those with at least one Achievement
        active_mrs = MR.objects.filter(achievement__isnull=False).distinct().count()
        sales = Achievement.objects.aggregate(total=Sum('est_value'))['total'] or 0
        pending_reports = Challenge.objects.filter(resolved=False).count()
        # Example team performance
        top_performer = Achievement.objects.order_by('-est_value').first()
        lowest_performer = Achievement.objects.order_by('est_value').first()
        team_average = Achievement.objects.aggregate(avg=Avg('est_value'))['avg'] or 0

        return Response({
            "total_mrs": total_mrs,
            "active_mrs": active_mrs,
            "sales": sales,
            "pending_reports": pending_reports,
            "team_performance": {
                "top_performer": str(top_performer.product) if top_performer else None,
                "top_sales": top_performer.est_value if top_performer else 0,
                "team_average": team_average,
                "lowest_performer": lowest_performer.product if lowest_performer else None,
                "lowest_sales": lowest_performer.est_value if lowest_performer else 0,
            }
        })

    @action(detail=True, methods=['get'], url_path='dashboard')
    def mr_dashboard(self, request, pk=None):
        mr = self.get_object()
        visits_today = VisitRes.objects.filter(plan__mr=mr).count()  # Add date filter for today
        sales_target = 75  # Example static, replace with logic
        orders = Achievement.objects.filter(mr=mr).count()
        reports = Challenge.objects.filter(mr=mr).count()

        return Response({
            "visits_today": visits_today,
            "sales_target": sales_target,
            "orders": orders,
            "reports": reports,
         })

class PatchOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'PATCH']

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class OutcomeCodeViewSet(viewsets.ModelViewSet):
    queryset = OutcomeCode.objects.all()
    serializer_class = OutcomeCodeSerializer
    permission_classes = [IsAuthenticated]

class PlantoMRViewSet(viewsets.ModelViewSet):
    queryset = PlantoMR.objects.all()
    serializer_class = PlantoMRSerializer
    permission_classes = [IsAuthenticated]

class VisitResViewSet(viewsets.ModelViewSet):
    queryset = VisitRes.objects.all()
    serializer_class = VisitResSerializer
    permission_classes = [IsAuthenticated]

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

class Voice_assistViewSet(viewsets.ModelViewSet):
    queryset= Voice_assist.objects.all()
    serializer_class=  Voice_assistSerializer
    permission_classes= [IsAuthenticated]
    