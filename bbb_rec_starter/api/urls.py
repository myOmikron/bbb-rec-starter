from django.urls import path

from api.views import *

urlpatterns = [
    path('startRecording', StartRecordingView.as_view())
]
