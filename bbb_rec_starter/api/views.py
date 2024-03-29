import json
import logging

from django.http import JsonResponse
from django.views import View

from rc_protocol import validate_checksum

from api.models import MeetingModel
from bbb_rec_starter import settings

logger = logging.getLogger("api")


class ScheduleRecordingView(View):

    def post(self, request):
        try:
            decoded = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "JSON could not be decoded"})

        if "checksum" not in decoded:
            return JsonResponse({"success": False, "message": "Parameter checksum is required but missing"}, status=401)
        checksum = decoded["checksum"]
        del decoded["checksum"]
        if not validate_checksum(
                request=decoded,
                checksum=checksum,
                shared_secret=settings.RCP_SECRET,
                salt="scheduleRecording",
                time_delta=settings.RCP_TIME_DELTA
        ):
            return JsonResponse({"success": False, "message": "You did not pass the checksum test"}, status=403)

        if "meeting_id" not in decoded:
            data = {"success": False, "result": "Missing parameter: meeting_id"}
            return JsonResponse(data, status=400, reason=data["result"])

        if MeetingModel.objects.filter(meeting_id=decoded["meeting_id"]).exists():
            return JsonResponse({"success": True, "message": "Meeting was already scheduled"}, status=304)
        MeetingModel.objects.create(meeting_id=decoded["meeting_id"])
        return JsonResponse({"success": True, "message": "Scheduled meeting"})
