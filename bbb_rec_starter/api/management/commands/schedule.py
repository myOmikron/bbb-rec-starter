import logging
from time import sleep

from django.core.management import BaseCommand

from api import scripts
from api.models import MeetingModel


logger = logging.getLogger("scheduler")


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            sleep(15)
            logger.info("Starting loop")
            meetings = MeetingModel.objects.all()
            if meetings.count() == 0:
                logger.info("No recordings to start, sleeping ...")
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

                logger.info(f"Status: {status} :: Response: {response}")
