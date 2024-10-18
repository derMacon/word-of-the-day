import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.controller.housekeeping_controller import trigger_complete_cycle
from src.utils.logging_config import app_log
import os

CRON_EXPRESSION = os.getenv('WOTD_HOUSEKEEPING_CRON', '* * * * *')


def configure_housekeeping_background_scheduler():
    if os.getenv('DEBUG_DISABLE_CRON', False):
        app_log.info('cron expression for housekeeping disabled')
    else:
        app_log.info(f'initializing background housekeeping scheduler with cron expression: {CRON_EXPRESSION}')
        scheduler = BackgroundScheduler()
        cron_trigger = CronTrigger.from_crontab(CRON_EXPRESSION)
        scheduler.add_job(trigger_complete_cycle, trigger=cron_trigger)
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
