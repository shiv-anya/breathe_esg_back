from django.urls import path
from .views import (
    upload_csv,
    get_activities,
    approve_activity,
    reject_activity,
    get_audits
)

urlpatterns = [
    path('upload/', upload_csv),
    path('activities/', get_activities),
    path('audits/', get_audits),
    path('approve/<int:id>/', approve_activity),
    path('reject/<int:id>/', reject_activity),
]