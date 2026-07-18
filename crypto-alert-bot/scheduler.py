"""
Scheduler for automated bot tasks using APScheduler.
"""

import asyncio
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from utils.logger import setup_logger

logger = setup_logger(__name__)


class BotScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(daemon=True)

    def schedule_interval_job(
        self,
        func: Callable,
        minutes: int,
        job_id: str,
    ) -> None:
        """Schedule a job to run at regular intervals."""
        try:
            self.scheduler.add_job(
                func,
                IntervalTrigger(minutes=minutes),
                id=job_id,
                name=f"{job_id} (every {minutes} min)",
                replace_existing=True,
            )
            logger.info("Scheduled job: %s (every %d minutes)", job_id, minutes)
        except Exception as error:
            logger.error("Failed to schedule job %s: %s", job_id, error)

    def schedule_cron_job(
        self,
        func: Callable,
        hour: int,
        minute: int,
        job_id: str,
    ) -> None:
        """Schedule a job to run at a specific time daily."""
        try:
            self.scheduler.add_job(
                func,
                CronTrigger(hour=hour, minute=minute),
                id=job_id,
                name=f"{job_id} (daily at {hour:02d}:{minute:02d})",
                replace_existing=True,
            )
            logger.info("Scheduled job: %s (daily at %02d:%02d)", job_id, hour, minute)
        except Exception as error:
            logger.error("Failed to schedule job %s: %s", job_id, error)

    def start(self) -> None:
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")

    def get_jobs(self) -> list:
        """Get list of scheduled jobs."""
        return self.scheduler.get_jobs()
