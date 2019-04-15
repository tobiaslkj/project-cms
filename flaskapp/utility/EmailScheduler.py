import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class EmailScheduler():
    # Register scheudling process
        def __init__(self):
            EmailScheduler.scheduler = BackgroundScheduler()
            EmailScheduler.scheduler.add_job(func=EmailScheduler.task, trigger="interval", minutes=60)
            print("Job registered and started")
            EmailScheduler.scheduler.start()
            atexit.register(EmailScheduler.shutdownTask)

        @staticmethod
        def task():
            from flaskapp.utility.ReportEmail import findReportContent
            resultDict = findReportContent()
            message = "Currently, there are {} incidents resolved and {} incidents still ongoing.".format(\
            resultDict.get("numOfResolvedIncident"), resultDict.get("numOfOngoingIncident"))
            
            from flaskapp.utility.EmailSender import send_email
            send_email(message)
            
            print("Job run at", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        
        @staticmethod
        def shutdownTask():
            print('shutting down email scheduler')
            EmailScheduler.scheduler.shutdown()
