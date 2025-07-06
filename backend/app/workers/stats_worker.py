from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.crud.stats import record_daily_stats

def run_job():
    db = SessionLocal()
    try:
        print("Running daily stats update...")
        record_daily_stats(db)
    finally:
        db.close()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_job, "interval", minutes=30)
    scheduler.start()
    print("Scheduler started.")
