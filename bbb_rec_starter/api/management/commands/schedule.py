import logging
from datetime import datetime
from time import sleep

from django.core.management import BaseCommand

from api import scripts
from api.models import MeetingModel


logger = logging.getLogger("scheduler")


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Starting loop")
        while True:
            sleep(15)
            meetings = MeetingModel.objects.all()
            if meetings.count() == 0:
                logger.debug("No recordings to start, sleeping ...")
                continue
            for meeting in meetings:
                logger.info(f"Scheduling meeting with id: {meeting.meeting_id}")
                response, status = scripts.start_recording(meeting.meeting_id)

                # Delete meeting from scheduling if:
                # - Recording was started successfully
                # - Meeting has recording not enabled
                # - Recording had already been started or is currently paused
                if status == 200 or status == 515 or status == 514:
                    meeting.delete()

                # Delete meeting if it is in db longer than 30 minutes
                if meeting.created.timestamp() + 30*60 < datetime.utcnow().timestamp():
                    logger.info(f"Removing meeting {meeting.meeting_id} as it can't be scheduled for 30min.")
                    meeting.delete()

                logger.info(f"Meeting:{meeting.meeting_id} :: Status: {status} :: Response: {response}")
