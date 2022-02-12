import logging

from django.http import JsonResponse
from django.views import View

from rc_protocol import validate_checksum

from api.models import MeetingModel
from bbb_rec_starter import settings

logger = logging.getLogger("api")


class ScheduleRecordingView(View):

    def post(self, request):
        if "checksum" not in request.POST:
            return JsonResponse({"success": False, "message": "Parameter checksum is required but missing"}, status=401)
        checksum = request.POST["checksum"]
        del request.POST["checksum"]
        if not validate_checksum(
                request=request.POST,
                checksum=checksum,
                shared_secret=settings.RCP_SECRET,
                salt="scheduleRecording",
                time_delta=settings.RCP_TIME_DELTA
        ):
            return JsonResponse({"success": False, "message": "You did not pass the checksum test"}, status=403)

        if "meeting_id" not in request.POST:
            data = {"success": False, "result": "Missing parameter: meeting_id"}
            return JsonResponse(data, status=400, reason=data["result"])

        meeting, created = MeetingModel.objects.get_or_create(meeting_id=request["meeting_id"])
        if not created:
            return JsonResponse({"success": True, "message": "Meeting was already scheduled"}, status=304)
        return JsonResponse({"success": True, "message": "Scheduled meeting"})
