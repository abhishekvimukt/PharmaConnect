# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.webhook, name='webhook'),
    
# ]
from django.urls import path
from .views import telegram_webhook

urlpatterns = [
    path('webhook/', telegram_webhook, name='telegram_webhook'),
]

