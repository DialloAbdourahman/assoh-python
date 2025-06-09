# scheduler.py
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # ✅ Use AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from tasks.cleanup_pending_orders import cleanup_pending_orders
from utils.config import cron_job_minutes_interval

# scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()  # ✅ Use async scheduler


def start_scheduler():
    scheduler.add_job(
        cleanup_pending_orders,
        CronTrigger(minute=f'*/{cron_job_minutes_interval}'), 
        id="cleanup_pending_orders",
        replace_existing=True
    )
    scheduler.start()