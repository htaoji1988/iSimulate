__author__ = 'Iamokthanks'

import threading
import Queue
import time
import iConf
import iSimulate
import datetime
import iSchedule
import traceback


class Scheduler(threading.Thread):
    def __init__(self, t_name, extraArgs):
        threading.Thread.__init__(self, name=t_name)
        self.extraArgs = extraArgs

    def run(self):
        print("THREAD_SCHEDULER {0} initialized at {1}".format(self.name, datetime.datetime.now()))
        try:
            sched = iSchedule.iSchedule()
            sched.initSchedule()
        except Exception as e:
            traceInfo = traceback.format_exc()
            print("**********Exception Info**********")
            print(e)
            print("**********Trackback Info**********")
            print(traceInfo)


class Producer(threading.Thread):
    def __init__(self, queueTask, t_name, extraArgs):
        threading.Thread.__init__(self, name=t_name)
        self.queueTask = queueTask
        self.extraArgs = extraArgs

    def run(self):
        print("THREAD_PRODUCER {0} initialized at {1}".format(self.name, datetime.datetime.now()))
        while True:
            try:
                iConf.ConfigurationX({}, self.queueTask)
            except Exception as e:
                traceInfo = traceback.format_exc()
                print("**********Exception Info**********")
                print(e)
                print("**********Trackback Info**********")
                print(traceInfo)
            time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self, queueTask, t_name, extraArgs):
        threading.Thread.__init__(self, name=t_name)
        self.queueTask = queueTask
        self.extraArgs = extraArgs

    def run(self):
        print("THREAD_COMSUMER {0} initialized at {1}".format(self.name, datetime.datetime.now()))
        time.sleep(1)
        while True:
            try:
                currentTask = self.queueTask.get(block=True, timeout=None)
                print("Thread:{0} Get {1} from Queue end".format(self.name, currentTask))
                iSimulate.Simulate(currentTask)
            except Exception as e:
                traceInfo = traceback.format_exc()
                print("**********Exception Info**********")
                print(e)
                print("**********Trackback Info**********")
                print(traceInfo)


class ThreadPool:
    def __init__(self, queueTask, poolSize, role, extraArgs):
        self.threads = []
        self.queueTask = queueTask
        self.poolSize = poolSize
        self.role = role
        self.extraArgs = extraArgs
        self.__createPool()

    def __createPool(self):
        if self.role == "PRODUCER":
            for i in range(1):
                self.threads.append(Producer(self.queueTask, "P{0}".format(i + 1), self.extraArgs))

        if self.role == "CONSUMER":
            for i in range(self.poolSize):
                self.threads.append(Consumer(self.queueTask, "C{0}".format(i + 1), self.extraArgs))
        if self.role == "SCHEDULE":
            for i in range(self.poolSize):
                self.threads.append(Scheduler("S{0}".format(i + 1), self.extraArgs))

        for i in self.threads:
            i.start()

    def joinPool(self):
        for i in self.threads:
            i.join()


class FlushLog(threading.Thread):
    pass


if __name__ == '__main__':
    queueTask = Queue.Queue(maxsize=1)
    pl = ThreadPool(queueTask=queueTask, poolSize=1, role="PRODUCER", extraArgs={})
    cl = ThreadPool(queueTask=queueTask, poolSize=1, role="CONSUMER", extraArgs={})
    s1 = ThreadPool(queueTask=queueTask, poolSize=1, role="SCHEDULE", extraArgs={})
