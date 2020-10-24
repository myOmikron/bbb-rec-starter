from django.http import JsonResponse
from django.views import View


class StartRecordingView(View):

    def post(self, request):
        data = {}
        return JsonResponse(data)
