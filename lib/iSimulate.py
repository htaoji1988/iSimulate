__author__ = 'iamok'

import pexpect
import sys
import os
import time
import traceback


class Simulate:
    def __init__(self, host):
        self.host = host
        self.RESULT_PATH = './result'
        self.__interact()

    def __interact(self):
        devGroupName = self.host['devGroup']['groupName']
        devGroupEnable = self.host['devGroup']['enable']
        devGroupEntry = self.host['devGroup']['devEntry']
        devPrompt = self.host['dev']['devPrompt']
        devName = self.host['dev']['devName']
        devIp = self.host['dev']['ip']
        # ---#
        dateToday = time.strftime('%Y%m%d', time.localtime(time.time()))
        destPath = self.RESULT_PATH + '/' + dateToday + '/' + devGroupName
        destFile = devGroupName + "_" + devName + "_" + devIp + '.txt'
        if not os.path.exists(destPath):
            try:
                os.makedirs(destPath)
            except Exception as e:
                traceInfo = traceback.format_exc()
                print("**********Exception Info**********")
                print(e)
                print("**********Trackback Info**********")
                print(traceInfo)
        resultFH = open(destPath + '/' + destFile, 'w+')
        # ---#
        resultFH.write("#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#\n")
        resultFH.write("#" + devGroupName + "," + devName + "," + devIp + "," + devGroupEntry + "\n")
        resultFH.write("#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#\n")
        # ---#
        devGroupEntry_C = devGroupEntry.strip()
        isSsh = devGroupEntry_C.startswith("ssh")
        child = self.__spawnEntry(devGroupEntry_C, isSsh, self.host, resultFH)
        if child:
            for cmd in self.host['cmds']:
                seq = cmd["seq"]
                send = cmd["send"]
                expect = cmd["expect"]
                self.__sendUnit(child, send, expect, resultFH)
            child.close()
        resultFH.close()
        # ---#

    def __sendUnit(self, child, send, expect, resultFH):
        child.sendline(send)
        try:
            index = child.expect([pexpect.TIMEOUT, pexpect.EOF, expect], timeout=3600)
            if index == 0:
                print("Connect Timeout")
                # ---#
                return False
            if index == 1:
                resultFH.write(child.before)
                return False
            if index == 2:
                print("execute success with expect")
                # ---#
                print(child.before)
                print(child.after)
                resultFH.write(child.before)
                resultFH.write(child.after)
                # ---#
                return True
            else:
                print("Unknown error")
                return False
        except Exception as e:
            traceInfo = traceback.format_exc()
            print("**********Exception Info**********")
            print(e)
            print("**********Trackback Info**********")
            print(traceInfo)

    '''Trust And No Trust'''

    def __sshLogin(self, child, password, devPrompt, resultFH):
        try:
            index = child.expect(
                ['Are you sure you want to continue connecting', '.*[pP]assword:', devPrompt, pexpect.TIMEOUT,
                 pexpect.EOF], timeout=10)
            if index == 0:
                print("SSH First Login")
                child.sendline('yes')
                index_r = child.expect([pexpect.TIMEOUT, pexpect.EOF, '.*[pP]assword:', devPrompt], timeout=10)
                if index_r == 0:
                    print("SSH First Login Connect Timeout")
                    return False
                elif index_r == 1:
                    resultFH.write(child.before)
                    print("SSH Login Unexpected EOF")
                    return False
                elif index_r == 2:
                    print("SSH First Login with Password")
                    resultFH.write(child.before)
                    resultFH.write(child.after)
                    return self.__sendUnit(child, password, devPrompt, resultFH)
                elif index_r == 3:
                    print("SSH First Login with Trust")
                    resultFH.write(child.before)
                    resultFH.write(child.after)
                    return True
                else:
                    print("SSH First Login Unknow Error")
                    return False
            elif index == 1:
                print("SSH No First Login with password")
                resultFH.write(child.before)
                resultFH.write(child.after)
                return self.__sendUnit(child, password, devPrompt, resultFH)
            elif index == 2:
                print("SSH No First Login with Trust")
                resultFH.write(child.before)
                resultFH.write(child.after)
                return True
            elif index == 3:
                print("SSh No First Login Connect Timeout")
                return False
            elif index == 4:
                print("SSH Login Unexpected EOF")
                resultFH.write(child.before)
                return False
            else:
                print("SSH unknown error")
                return False
        except Exception as e:
            traceInfo = traceback.format_exc()
            print("**********Exception Info**********")
            print(e)
            print("**********Trackback Info**********")
            print(traceInfo)

    def __spawnEntry(self, devGroupEntry, isSsh, host, resultFH):

        devGroupEntry = host['devGroup']['devEntry']
        devPrompt = host['dev']['devPrompt']

        child = pexpect.spawn(devGroupEntry)
        child.logfile_send = sys.stdout
        child.delaybeforesend = 1

        if isSsh:
            devPassword = host['dev']['password']
            resultSign = self.__sshLogin(child, devPassword, devPrompt, resultFH)
            if resultSign == True:
                return child
            else:
                resultFH.write("Login Failed\r\n")
                return False
        else:
            try:
                index = child.expect([pexpect.TIMEOUT, pexpect.EOF, devPrompt], timeout=10)
                if index == 0:
                    print("Login Timeout")
                    return False
                elif index == 1:
                    print("Login Unexpected EOF")
                    resultFH.write(child.before)
                    return False
                elif index == 2:
                    resultFH.write(child.before)
                    resultFH.write(child.after)
                    return child
                else:
                    return False
            except Exception as e:
                traceInfo = traceback.format_exc()
                print("**********Exception Info**********")
                print(e)
                print("**********Trackback Info**********")
                print(traceInfo)


'''Unit Test'''


def test():
    Simulate(Hosts[0])


if __name__ == '__main__':
    test()
