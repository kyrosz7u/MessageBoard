from typing import List, Callable

class cmdParser:
    def __init__(self):
        self.cmdDict = dict()

    def addCmd(self, cmdStr:str):
        def decorator(view_func: Callable[[List[str]], int]):
            if len(cmdStr) != 0:
                self.cmdDict[cmdStr] = view_func
            return view_func
        return decorator

    def parserCmd(self):
        print('>> ', end='')
        cmdstr = input()
        paramList = cmdstr.split(" ")
        if len(paramList)<1:
            return -1;

        if paramList[0] in self.cmdDict:
            return self.cmdDict[paramList[0]](paramList[1:])




