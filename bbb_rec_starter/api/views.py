from django.conf import settings
from django.http import JsonResponse
from django.views import View

from api.scripts import start_recording


class StartRecordingView(View):

    def post(self, request):
        data = {}
        return_code = 200
        user = "StartRecordingUser"
        if "secret" in request.POST:
            if request.POST["secret"] == settings.BBB_SECRET:
                if "meeting_id" in request.POST:
                    if "password" in request.POST:
                        data["success"] = "true"
                        data["result"] = f"Joining meeting {request.POST['meeting_id']} with " \
                                         f"password {request.POST['password']} as user {user}."
                        start_recording(request.POST["meeting_id"], request.POST["password"], user)
                    else:
                        data["success"] = "false"
                        data["result"] = "Missing parameter: password"
                        return_code = 400
                else:
                    data["success"] = "false"
                    data["result"] = "Missing parameter: meeting_id"
                    return_code = 400
            else:
                data["success"] = "false"
                data["result"] = "Unauthorized"
                return_code = 401
        else:
            data["success"] = "false"
            data["result"] = "Missing parameter: secret"
            return_code = 400
        return JsonResponse(data, status=return_code)
