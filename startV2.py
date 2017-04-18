__author__ = 'iamok'

from lib import iThreadPool, iSchedule
import Queue
import time


if __name__ == '__main__':

    try:
        """Init Queue"""
        queueTask = Queue.Queue(maxsize=1000)
        """Init Producer"""
        pl = iThreadPool.ThreadPool(queueTask=queueTask, poolSize=1, role="PRODUCER", extraArgs={})
        """Init Consumer"""
        cl = iThreadPool.ThreadPool(queueTask=queueTask, poolSize=10, role="CONSUMER", extraArgs={})
        """Init Schedule"""
        s1 = iThreadPool.ThreadPool(queueTask=queueTask, poolSize=1, role="SCHEDULE", extraArgs={})
    except Exception as e:
        traceInfo = traceback.format_exc()
        print("**********Exception Info**********")
        print(e)
        print("**********Trackback Info**********")
        print(traceInfo)

