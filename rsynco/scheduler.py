import threading
import logging
import time
import schedule
from rsynco.libs.repositories.job_repository import JobRepository
from rsynco.libs.repositories.host_repository import HostRepository
from rsynco.libs.rsync import Rsync, NoHostException
from rsynco import job_queue
import queue
from datetime import datetime


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

        try:
            self._Rsync.process(
                self._HostRepository.get_host(job['from_host']),
                job['from_path'],
                self._HostRepository.get_host(job['to_host']),
                job['to_path']
            )
        except NoHostException as no_host:
            logging.error(no_host)

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
        job_schedule = job['schedule']
        if job_schedule['type'] == 'once':
            self.add_schedule_once(
                job['name'],
                job_schedule['date'],
                int(job_schedule['hour']),
                int(job_schedule['minute']),
                job_schedule['meridiem']
            )
        elif job_schedule['type'] == 'day':
            self.add_schedule_day(
                job['name'],
                int(job_schedule['hour']),
                int(job_schedule['minute']),
                job_schedule['meridiem']
            )
        elif job_schedule['type'] == 'week':
            self.add_schedule_week(
                job['name'],
                int(job_schedule['week']),
                int(job_schedule['weekFrequency']),
                job_schedule['days'],
                int(job_schedule['hour']),
                int(job_schedule['minute']),
                job_schedule['meridiem']
            )
        elif job_schedule['type'] == 'month':
            self.add_schedule_month(
                job['name'],
                int(job_schedule['month']),
                int(job_schedule['monthFrequency']),
                job_schedule['days'],
                int(job_schedule['hour']),
                int(job_schedule['minute']),
                job_schedule['meridiem']
            )
        elif job_schedule['type'] == 'hour':
            self.add_schedule_hour(
                job['name'],
                int(job_schedule['minute'])
            )
        elif job_schedule['type'] == 'second':
            self.add_schedule_second(
                job['name'],
                int(job_schedule['secondFrequency'])
            )

    def delete_schedule(self, job_name):
        logging.debug('Deleting job schedule {}'.format(job_name))
        schedule.clear(job_name)

    def update_schedule(self, job_name):
        logging.debug('Updating job schedule {}'.format(job_name))
        self.delete_schedule(job_name)
        self.add_schedule(job_name)

    def add_schedule_once(self, job_name, date, hour, minute, meridiem):
        """
        TODO: Make this run only once
        """
        logging.debug('Adding once-off schedule for job {}'.format(job_name))
        schedule.every()\
            .day\
            .at(self.meridiem_time_to_24_hour(hour, minute, meridiem))\
            .do(self.run_job, job_name)\
            .tag(job_name)
        logging.debug('Added job')

    def add_schedule_day(self, job_name, hour, minute, meridiem):
        logging.debug('Adding daily schedule for job {}'.format(job_name))
        schedule.every()\
            .day\
            .at(self.meridiem_time_to_24_hour(hour, minute, meridiem))\
            .do(self.run_job, job_name)\
            .tag(job_name)

    def add_schedule_week(self, job_name, start_week, week_frequency, days, hour, minute, meridiem):
        """
        TODO: start_week not used, remove from UI
        TODO: Schedule only performs one day of the week rather than select days of the week
        """
        logging.debug('Adding weekly schedule for job {}'.format(job_name))
        schedule.every(week_frequency)\
            .monday\
            .at(self.meridiem_time_to_24_hour(hour, minute, meridiem))\
            .do(self.run_job, job_name)\
            .tag(job_name)

    def add_schedule_month(self, job_name, start_month, month_frequency, day, hour, minute, meridiem):
        """
        Hmm, schedule doesn't do every month. Cheat and do every 30 days...
        TODO: start_month is unused at the moment, maybe remove it from the UI
        """
        logging.debug('Adding monthly schedule for job {}'.format(job_name))
        schedule.every(month_frequency * 30)\
            .days()\
            .at(self.meridiem_time_to_24_hour(hour, minute, meridiem))\
            .do(self.run_job, job_name)\
            .tag(job_name)

    def add_schedule_hour(self, job_name, minute):
        logging.debug('Adding schedule for job {} to run every {} minute pas the hour'.format(job_name, minute))
        schedule.every()\
            .hours\
            .at('0:{}'.format(minute))\
            .do(self.run_job, job_name)\
            .tag(job_name)

    def add_schedule_second(self, job_name, second_frequency):
        logging.debug('Adding schedule for job {} to run ever {} seconds'.format(job_name, second_frequency))
        schedule.every(second_frequency)\
            .seconds\
            .do(self.run_job, job_name)\
            .tag(job_name)

    def meridiem_time_to_24_hour(self, hour, minute, meridiem):
        parsed_datetime = datetime.strptime('{:02d}:{:02d} {}'.format(hour, minute, meridiem), '%I:%M %p')
        return parsed_datetime.strftime('%H:%M')
