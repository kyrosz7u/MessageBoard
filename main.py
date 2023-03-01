from cmdParser import cmdParser
from sqlManager import SQLManager
from MsgBoard import User, Comment, Likemsg

from typing import List


parser = cmdParser()

MessageBoardDB = SQLManager(dbhost='localhost',
                            dbuser='root',
                            password='zhuxiyu123',
                            database='MessageBoard')

currentUser = User(MessageBoardDB)

Commenter = Comment(currentUser, MessageBoardDB)
MsgLiker = Likemsg(currentUser, MessageBoardDB)

parser.addCmd("login", currentUser.login)
parser.addCmd("logon", currentUser.logon)
parser.addCmd("logout", currentUser.logout)
parser.addCmd("add_msg", Commenter.add_msg)
parser.addCmd("del_msg", Commenter.del_msg)
parser.addCmd("like_msg", MsgLiker.like_msg)
parser.addCmd("unlike_msg", MsgLiker.unlike_msg)

# @parser.addCmd("add_msg")
# def add_msg(parsersList: List[str]):
#     pass
#
# @parser.addCmd("del_msg")
# def del_msg(parsersList: List[str]):
#     pass
#
# @parser.addCmd("like_msg")
#
# @parser.addCmd("unlike_msg")

isExit = False
def exit(parsersList: List[str]):
    global isExit
    isExit = True
    return 0


def list(parsersList: List[str]):
    _n = 1
    if len(parsersList) > 1:
        print('输入参数有误')
        return -1;
    if len(parsersList) != 0:
        _n = int(parsersList[0])

    # 查询留言表中的uid和likedNum，并按照点赞数降序排列
    res, data = MessageBoardDB.request(
        f'select mid, likedNum from messageInfo order by likedNum desc'
    )

    i = 1
    while i < _n:
        i=i+1

    ## 每页显示3条留言
    idx = (i-1)*3
    end = idx + 3

    midList = []
    while idx < len(data) and idx < end:
        midList.append(data[idx]['mid'])
        idx = idx+1

    # [123,456] --> '(123,456)'
    midList = str(tuple(midList))

    res, data = MessageBoardDB.request(
        f'select mid,nickname,likedNum,messageDate,info from messageInfo where mid in {midList}'
    )

    # 输出留言
    for item in data:
        for each in item:
            print(each, ':', item[each])
        print('')


parser.addCmd("exit", exit)
parser.addCmd("q", exit)
parser.addCmd("list", list)

if __name__ == '__main__':
    while not isExit:
        parser.parserCmd()

    MsgLiker.exit()
    print('Bye')

    pass
