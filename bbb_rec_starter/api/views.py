from django.conf import settings
from django.http import JsonResponse
from django.views import View

from api.scripts import start_recording


class StartRecordingView(View):

    def post(self, request):
        data = {}
        user = "StartRecordingUser"
        if "secret" in request.POST:
            if request.POST["secret"] == settings.BBB_SECRET:
                if "meeting_id" in request.POST:
                    if "password" in request.POST:
                        status, return_code = start_recording(request.POST["meeting_id"], request.POST["password"], user)
                        if return_code != 200:
                            data["success"] = "false"
                            data["result"] = f"{status}"
                        else:
                            data["success"] = "true"
                            data["result"] = f"Joining meeting {request.POST['meeting_id']} with " \
                                             f"password {request.POST['password']} as user {user}."
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
        return JsonResponse(data, status=return_code, reason=status)
