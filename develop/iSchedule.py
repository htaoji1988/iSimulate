__author__ = 'iamok'

from apscheduler.scheduler import Scheduler
import time
import re
import shutil


class iSchedule:
    def __init__(self):
        self.sched = Scheduler()
        self.sched.start()


    def __moveToWorking(self):
        pass

    def __job_function(self, **kwargs):
        print(kwargs['taskFile'])
        print("Move Task {0} to working directory".format(kwargs['taskFile'][7]))
        srcFile = '../conf/workSchedule/' + kwargs['taskFile'][7]
        dstFile = '../conf/working/' + kwargs['taskFile'][7]

        shutil.copy(srcFile, dstFile)

    def initTask(self):
        for line in open("../conf/workSchedule/crontab.list"):
            if not re.match('^#', line):
                timeArray = re.split('\s*', line)
                print(timeArray)
                second = timeArray[0]
                minute = timeArray[1]
                hour = timeArray[2]
                day = timeArray[3]
                month = timeArray[4]
                year = timeArray[5]
                dayOfWeek = timeArray[6]
                taskFile = timeArray[7]

                self.sched.add_cron_job(self.__job_function, second=second, minute=minute, hour=hour, day=day,
                                        month=month, year=year, day_of_week=dayOfWeek, kwargs={'taskFile': timeArray})

        while True:
            time.sleep(1000000)


if __name__ == '__main__':
    sched = iSchedule()
    sched.initTask()