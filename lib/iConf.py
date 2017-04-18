__author__ = 'Iamokthanks'

import xml.etree.ElementTree as xmlet
import Queue
import os
import shutil


class ConfigurationX:
    def __init__(self, confFile, queueTask):
        self.CONF_PATH = './conf/'
        self.WORKING_PATH = self.CONF_PATH + 'working/'
        self.WORKED_PATH = self.CONF_PATH + 'worked/'
        self.WORKSCHEDULE_PATH = self.CONF_PATH + 'workSchedule/'
        self.confFile = confFile
        self.queueTask = queueTask
        self.__createQueueTask()

    def __mapping(self, dictSrc, dictMap):
        for key, value in dictSrc.items():
            for key_m, value_m in dictMap.items():
                dictSrc[key] = dictSrc[key].replace("=" + key_m + "=", value_m)
        return dictSrc

    def __createQueueTask(self):

        workingFiles = os.listdir(self.WORKING_PATH)
        taskFiles = [x for x in workingFiles if os.path.isfile(self.WORKING_PATH + x)]

        for taskFile in taskFiles:
            try:
                self.__dealSingleFile(taskFile)
            except Exception, exception:
                print(exception)

    def __dealSingleFile(self, taskFile):
        srcFullName = self.WORKING_PATH + taskFile
        dstFullName = self.WORKED_PATH + taskFile
        root = xmlet.parse(srcFullName).getroot()

        '''deal devGroupNodes'''
        devGroupNodes = root.findall("devGroup")
        for devGroupNode in devGroupNodes:
            '''deal devNodes'''
            devNodes = devGroupNode.find("devSeq").findall("dev")
            for devNode in devNodes:
                dictDevPairs = dict(devNode.items())
                if dictDevPairs != {}:
                    '''devGroup'''
                    dictDevGroupPairs = dict(devGroupNode.items())
                    dictDevGroupPairs = self.__mapping(dictDevGroupPairs, dictDevPairs)
                    ''' cmd'''
                    cmds = []
                    cmdNodes = devGroupNode.find("cmdSeq").findall("cmd")
                    for cmdNode in cmdNodes:
                        dictCmdPairs = dict(cmdNode.items())
                        if dictCmdPairs != {}:
                            dictCmdPairs = self.__mapping(dictCmdPairs, dictDevPairs)
                            cmds.append(dictCmdPairs)

                    host = {"devGroup": dictDevGroupPairs, "dev": dictDevPairs, "cmds": cmds}
                    self.queueTask.put(host, block=True, timeout=None)

        print("MOVE {0} TO {1}".format(self.WORKING_PATH + taskFile, self.WORKED_PATH + taskFile))
        # shutil.move(srcFullName, self.WORKED_PATH)
        os.rename(srcFullName, dstFullName)


"""Unit Test"""


def test():
    queueTask = Queue.Queue()
    conf = ConfigurationX("../conf/devGroups.xml", queueTask)

    while True:
        try:
            print(queueTask.get(block=False))
        except Queue.Empty:
            exit()


if __name__ == '__main__':
    test()
