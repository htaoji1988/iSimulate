__author__ = 'Iamokthanks'

import iSchedule


if __name__ == '__main__':
    print("Hello World")
    sched = iSchedule.iSchedule()
    sched.initTask()

"""
from apscheduler.scheduler import Scheduler
import time

sched = Scheduler()
sched.start()


def job_fucntion():
    print("Hello.Python")

def job_2():
    print("Hello.Perl")

sched.add_cron_job(job_fucntion, second='*', hour='*', day='*')
sched.add_cron_job(job_2, second='*/10', hour='*', day='*')


while True:
    time.sleep(1)
"""

