import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class EmailScheduler():
    # Register scheudling process
        def __init__(self):
            EmailScheduler.scheduler = BackgroundScheduler()
            EmailScheduler.scheduler.add_job(func=EmailScheduler.task, trigger="interval", seconds=10)
            print("Job registered and started")
            EmailScheduler.scheduler.start()
            atexit.register(EmailScheduler.shutdownTask)

        @staticmethod
        def task():
            print("Job run at", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        
        @staticmethod
        def shutdownTask():
            print('shutting down email scheduler')
            EmailScheduler.scheduler.shutdown()
