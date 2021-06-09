from django.conf import settings
from django.http import JsonResponse
from django.views import View

from api.scripts import start_recording


class StartRecordingView(View):

    def post(self, request):
        user = "StartRecordingUser"

        if "secret" not in request.POST:
            data = {"success": False, "result": "Missing parameter: secret"}
            return JsonResponse(data, status=400, reason=data["result"])

        if request.POST["secret"] != settings.BBB_SECRET:
            data = {"success": False, "result": "Unauthorized"}
            return JsonResponse(data, status=401, reason=data["result"])

        if "meeting_id" not in request.POST:
            data = {"success": False, "result": "Missing parameter: meeting_id"}
            return JsonResponse(data, status=400, reason=data["result"])

        if "password" not in request.POST:
            data = {"success": False, "result": "Missing parameter: password"}
            return JsonResponse(data, status=400, reason=data["result"])

        status, return_code = start_recording(request.POST["meeting_id"], request.POST["password"], user)
        if return_code != 200:
            data = {"success": False, "result": f"{status}"}
        else:
            data = {"success": True, "result": f"Joining meeting {request.POST['meeting_id']} with password "
                                               f"{request.POST['password']} as user {user}."}
        return JsonResponse(data, status=return_code, reason=data["result"])
