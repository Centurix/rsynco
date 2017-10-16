import threading
import logging
import time
import schedule


class Scheduler(threading.Thread):
    def run_job(self):
        logging.info('Running a scheduled job...')

    def run(self):
        logging.info('Starting scheduler thread...')
        self.addSchedules()
        while True:
            schedule.run_pending()
            time.sleep(10)

    def addSchedules(self):
        logging.info('Loading schedules...')
        schedule.every(10).seconds.do(self.run_job)
