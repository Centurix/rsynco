import schedule
import time

"""
xth minute past every hour
xth hour every day
Every Monday
Every second Tuesday
First Monday of the month
First of every month
Last day of the month
First of every second month
1st January of each year

Minute: Specific minute, every x minutes
Hour: Specific hour, every x hours
Day
Month
Year

https://schedule.readthedocs.io/en/stable/

Threading the scheduler while running cherrypy in the main thread.

import cherrypy
import thread
import time

def daemon():
   while 1:
       do_periodic_stuff()
       time.sleep(seconds)

cherrypy.root = my_cherrypy_root()
thread.start_new_thread(daemon)
cherrypy.server.start()
"""


def job():
    print("I'm working...")


schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


