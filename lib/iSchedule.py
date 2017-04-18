__author__ = 'iamok'

from apscheduler.scheduler import Scheduler
import time
import re
import shutil
import os


class iSchedule:
    def __init__(self):
        self.CONF_PATH = './conf/'
        self.WORKING_PATH = self.CONF_PATH + 'working/'
        self.WORKED_PATH = self.CONF_PATH + 'worked/'
        self.WORKSCHEDULE_PATH = self.CONF_PATH + 'workSchedule/'

        self.sched = Scheduler()
        self.sched.start()

    def __moveToWorking(self):
        pass

    def __job_function(self, **kwargs):
        print("@execute job {0}".format(kwargs['taskFile']))
        print("Move Task {0} to working directory".format(kwargs['taskFile'][7]))
        srcFile = self.WORKSCHEDULE_PATH + kwargs['taskFile'][7]
        dstFile = self.WORKING_PATH

        if os.path.isfile(srcFile):
            print("COPY,[{0}],[{1}]".format(srcFile, dstFile))
            shutil.copy(srcFile, dstFile)
        else:
            print("Job Failed:{0},not exist please check".format(srcFile))

    def initSchedule(self):
        while True:

            print("===Begin To Loading Schedules===")
            currentJobs = self.sched.get_jobs()

            if currentJobs:
                self.sched.unschedule_func(self.__job_function)

            patten = re.compile("""
                ^\s*((\d{1,2}(,\d{1,2})*)|(\d{1,2}-\d{1,2}(/\d{1,2})?)|(\*(/\d{1,2})?))\s+ #second
                ((\d{1,2}(,\d{1,2})*)|(\d{1,2}-\d{1,2}(/\d{1,2})?)|(\*(/\d{1,2})?))\s+ #minute
                ((\d{1,2}(,\d{1,2})*)|(\d{1,2}-\d{1,2}(/\d{1,2})?)|(\*(/\d{1,2})?))\s+ #hour
                ((\d{1,2}(,\d{1,2})*)|(\d{1,2}-\d{1,2}(/\d{1,2})?)|(\*(/\d{1,2})?))\s+ #day
                ((\d{1,2}(,\d{1,2})*)|(\d{1,2}-\d{1,2}(/\d{1,2})?)|(\*(/\d{1,2})?))\s+ #month
                ((\d{1,4}(,\d{1,4})*)|(\d{1,4}-\d{1,4}(/\d{1,4})?)|(\*(/\d{1,4})?))\s+ #year
                ((\d(,\d)*)|(\d-\d(/\d)?)|(\*(/\d)?))\s+ #day_of_week
                ([^\*])+$
            """, re.X)

            for line in open(self.WORKSCHEDULE_PATH + "crontab.list"):

                line = line.strip()

                match = patten.match(line)
                if match:
                    timeArray = re.split('\s+', line)
                    second = timeArray[0]
                    minute = timeArray[1]
                    hour = timeArray[2]
                    day = timeArray[3]
                    month = timeArray[4]
                    year = timeArray[5]
                    dayOfWeek = timeArray[6]
                    taskFile = timeArray[7]

                    self.sched.add_cron_job(self.__job_function, second=second, minute=minute, hour=hour, day=day,
                                            month=month, year=year, day_of_week=dayOfWeek,
                                            kwargs={'taskFile': timeArray})
                    print("++Add Line {0}".format(line))

                else:
                    print("Ommit Line:{0}".format(line))
            print("===Loading Schedule Compplete==")
            # print(self.sched.print_jobs())
            time.sleep(10)


if __name__ == '__main__':
    sched = iSchedule()
    sched.initSchedule()
    while True:
        time.sleep(1)
