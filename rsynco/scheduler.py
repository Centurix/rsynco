import threading
import logging
import time
import schedule
from rsynco.libs.repositories.job_repository import JobRepository
from rsynco.libs.repositories.host_repository import HostRepository
from rsynco.libs.rsync import Rsync
from rsynco import job_queue
import queue


"""
Every X seconds, minutes, hours
===============================

Two arguments
* Number of seconds/minutes/hours per interval
* Job name
"""


class Scheduler(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._JobRepository = JobRepository()
        self._HostRepository = HostRepository()
        self._Rsync = Rsync()

    def run_job(self, job_name):
        logging.info('Running job: {}...'.format(job_name))
        self._JobRepository.reload()
        job = self._JobRepository.get_job(job_name)
        logging.debug('Scheduler: Starting rsync from host {} to host {}'.format(job['from_host'], job['to_host']))

        self._Rsync.process(
            self._HostRepository.get_host(job['from_host']),
            job['from_path'],
            self._HostRepository.get_host(job['to_host']),
            job['to_path']
        )

    def run(self):
        logging.info('Starting scheduler thread...')
        self.add_schedules()
        while True:
            logging.debug('FETCHING QUEUE MESSAGES')
            try:
                data = job_queue.get_nowait()

                logging.debug('======================FETCHED DATA======================')
                logging.debug(data)
                logging.debug('======================DATA FETCHED======================')
                if data != '':
                    logging.debug('GOT A QUEUE JOB {}, UPDATING THE SCHEDULER!'.format(data))
                    self.update_schedule(data)

            except queue.Empty as e:
                logging.debug('Nothing in the queue...')
                logging.debug(e)

            logging.debug('======================RUNNING PENDING SCHEDULES======================')
            schedule.run_pending()
            time.sleep(10)

    def add_schedules(self):
        logging.info('Loading schedules...')
        self._JobRepository.reload()
        jobs = self._JobRepository.get_jobs()
        logging.debug('Loaded {} jobs'.format(len(jobs)))
        for job in jobs:
            self.add_schedule(job['name'])

    def add_schedule(self, job_name):
        logging.debug('Adding job schedule {}'.format(job_name))
        self._JobRepository.reload()
        job = self._JobRepository.get_job(job_name)
        if job['repeat'] == 'seconds':
            self.add_schedule_seconds(int(job['repeat_every']), job['name'])
        elif job['repeat'] == 'minutes':
            self.add_schedule_minutes(int(job['repeat_every']), job['name'])
        elif job['repeat'] == 'hours':
            self.add_schedule_hours(int(job['repeat_every']), job['name'])

    def delete_schedule(self, job_name):
        logging.debug('Deleting job schedule {}'.format(job_name))
        schedule.clear(job_name)

    def update_schedule(self, job_name):
        logging.debug('Updating job schedule {}'.format(job_name))
        self.delete_schedule(job_name)
        self.add_schedule(job_name)

    def add_schedule_seconds(self, seconds, job_name):
        logging.debug('Adding schedule for job {} for every {} seconds'.format(job_name, seconds))
        schedule.every(seconds).seconds.do(self.run_job, job_name).tag(job_name)
        logging.debug(schedule.jobs)

    def add_schedule_minutes(self, minutes, job_name):
        logging.debug('Adding schedule for job {} for every {} minutes'.format(job_name, minutes))
        logging.debug(schedule.jobs)
        schedule.every(minutes).minutes.do(self.run_job, job_name).tag(job_name)
        for job in schedule.jobs:
            logging.debug(job.tags)

    def add_schedule_hours(self, hours, job_name):
        logging.debug('Adding schedule for job {} for every {} hours'.format(job_name, hours))
        schedule.every(hours).hours.do(self.run_job, job_name).tag(job_name)
        logging.debug(schedule.jobs)
