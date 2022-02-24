import logging
from datetime import datetime
from time import sleep

from django.core.management import BaseCommand

from api import scripts
from api.models import MeetingModel
from api.scripts import Fred

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
                f = Fred(meeting.meeting_id)
                f.start()
                f.join(timeout=60.0)
                if f.is_alive():
                    response, status = f"Timeout was reached for {meeting.meeting_id}", -1
                    f.kill()
                else:
                    response, status = f.ret

                # Delete meeting from scheduling if:
                # - Recording was started successfully
                # - Meeting has recording not enabled
                # - Recording had already been started or is currently paused
                if status == 200 or status == 515 or status == 514:
                    meeting.delete()

                # Delete meeting if it is in db longer than 30 minutes
                elif meeting.created.timestamp() + 30*60 < datetime.utcnow().timestamp():
                    logger.info(f"Removing meeting {meeting.meeting_id} as it can't be scheduled for 30min.")
                    meeting.delete()

                logger.info(f"Meeting:{meeting.meeting_id} :: Status: {status} :: Response: {response}")
