import logging
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.views import View

from api.models import Flag
from api.scripts import start_recording


logger = logging.getLogger("api")


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

        flag = Flag.objects.first()
        if flag is None:
            flag = Flag.objects.create()
        else:
            if flag.created.timestamp() + 60 < datetime.utcnow().timestamp():
                flag.delete()
                flag = Flag.objects.create()
        status, return_code = start_recording(request.POST["meeting_id"], request.POST["password"], user)
        flag.delete()
        if return_code != 200:
            data = {"success": False, "result": f"{status}"}
            logger.info(f"Request failed: {status}")
        else:
            data = {"success": True, "result": f"Joining meeting {request.POST['meeting_id']} with password "
                                               f"{request.POST['password']} as user {user}."}
            logger.info(f"Joining meeting {request.POST['meeting_id']} with password "
                        f"{request.POST['password']} as user {user}.")

        return JsonResponse(data, status=return_code, reason=data["result"])
