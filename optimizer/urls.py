from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MRViewSet, DoctorViewSet, OutcomeCodeViewSet,
    PlantoMRViewSet, VisitResViewSet, AchievementViewSet,
    ChallengeViewSet, ExpenseViewSet, MedicineViewSet,
    Voice_assistViewSet
)

router = DefaultRouter()
router.register(r'mrs', MRViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'outcome-codes', OutcomeCodeViewSet)
router.register(r'plans', PlantoMRViewSet)
router.register(r'visits', VisitResViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'challenges', ChallengeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'voice-assist', Voice_assistViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
