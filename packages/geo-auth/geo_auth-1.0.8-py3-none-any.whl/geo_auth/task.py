import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler

from .database import download_database,run_first_time_setup

def start_scheduler():
    scheduler = BackgroundScheduler()
    run_first_time_setup()
    
    scheduler.add_job(download_database, "interval", hours=6, id="database_task", replace_existing=True)

    scheduler.start()
    logging.info("✅ APScheduler started successfully!")