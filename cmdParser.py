from typing import List, Callable

class cmdParser:
    def __init__(self):
        self.cmdDict = dict()

    def addCmd(self, cmdStr:str, callback):
        if len(cmdStr) != 0:
            self.cmdDict[cmdStr] = callback


    def parserCmd(self):
        print('>> ', end='')
        cmdstr = input()
        paramList = cmdstr.split(" ")
        if len(paramList)<1:
            return -1;

        if paramList[0] in self.cmdDict:
            return self.cmdDict[paramList[0]](paramList[1:])




