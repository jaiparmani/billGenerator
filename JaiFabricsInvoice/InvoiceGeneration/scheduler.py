import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("InvoiceGeneration.backup")

_scheduler = None


def start():
    global _scheduler
    if _scheduler is not None:
        return

    from . import backup

    _scheduler = BackgroundScheduler(timezone="UTC", daemon=True)
    _scheduler.add_job(
        backup.run_daily_backup,
        trigger=CronTrigger(hour=18, minute=30),
        id="daily_db_backup",
        replace_existing=True,
        misfire_grace_time=3600,
    )
    _scheduler.start()
    logger.info("Daily backup scheduler started (runs 18:30 UTC)")
