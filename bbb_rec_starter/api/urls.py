from django.urls import path

from api.views import *

urlpatterns = [
    path('scheduleRecording', ScheduleRecordingView.as_view())
]
