from cmdParser import cmdParser
from user import User
from sqlManager import SQLManager
from typing import List

parser = cmdParser()
currentUser = User()
MessageBoardDB = SQLManager(dbhost='localhost',
                            dbuser='root',
                            password='zhuxiyu123',
                            database='MessageBoard')
isExit = False


@parser.addCmd("exit")
def exit(parsersList: List[str]):
    global isExit
    isExit=True
    return 0


@parser.addCmd("logon")
def logon(parsersList: List[str]):
    if len(parsersList) != 3:
        print('输入参数有误')
        return -1;
    res,_ = MessageBoardDB.request(
        f'insert into users(username,nickname,password,createDate) '
        f'values("{parsersList[0]}","{parsersList[1]}","{parsersList[2]}",NOW())'
    )

    if res == 1:
        print('注册成功')
    else:
        print('注册失败')
    return 0


@parser.addCmd("login")
def login(parsersList: List[str]):
    if len(parsersList) != 2:
        print('输入参数有误')
        return -1;

    if currentUser.isLogin:
        print('已经有用户登录了')
        return -1;

    res, data = MessageBoardDB.request(
        f'select *  from users where username="{parsersList[0]}" and password = "{parsersList[1]}"'
    )

    if res >= 1:
        data = data[0]
        currentUser.setUser(
            username=data['username'],
            nickname=data['nickname'],
            uid=int(data['uid']),
            createDate=data['createDate']
        )
        print('登录成功')
    else:
        print('登录失败')
    return 0

@parser.addCmd("logout")
def logout(parsersList: List[str]):
    currentUser.Logout()

@parser.addCmd("add_msg")
def add_msg(parsersList: List[str]):
    if not currentUser.isLogin:
        print('请先登录')
        return -1;

    # parsersList中保存了按空格拆分的留言info
    # 需要恢复原来的内容
    msgStr = ''
    for i in range(len(parsersList)-1):
        msgStr += parsersList[i]+' '
    msgStr += parsersList[-1]

    res, data = MessageBoardDB.request(
        f'insert into messageInfo (uid,nickname,likedNum,messageDate,info) '
        f'values ("{currentUser.uid}","{currentUser.nickname}",0,NOW(),"{msgStr}")'
    )

    print(res,data)


@parser.addCmd("del_msg")
def del_msg(parsersList: List[str]):
    if len(parsersList) != 1:
        print('输入参数有误')
        return -1;
    _mid = int(parsersList[0])

    res, data = MessageBoardDB.request(
        f'select uid from messageInfo where mid={_mid}'
    )

    if res<1 or data[0]['uid']!=currentUser.uid:
        print('删除失败')
        return -1

    res, data = MessageBoardDB.request(
        f'delete from messageInfo where mid={_mid}'
    )

    if res < 1:
        print('删除失败')
        return -1

    print('登录成功')
    return 0

@parser.addCmd("list")
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
        f'select nickname,likedNum,messageDate,info from messageInfo where mid in {midList}'
    )

    # 输出留言
    for item in data:
        for each in item:
            print(each, ':', item[each])
        print('')


def updateLikedNum(_mid):
    # 查询该留言的点赞人数
    res, data = MessageBoardDB.request(
        f'select count(uid) from liked where mid={_mid}'
    )

    if res < 1:
        return -1

    _likedNum = data[0]['count(uid)']

    # 更新点赞人数
    res, _ = MessageBoardDB.request(
        f'update messageInfo set likedNum={_likedNum} where mid={_mid}'
    )
    print("updateLikedNumRes: ",res)


@parser.addCmd("like_msg")
def like_msg(parsersList: List[str]):
    if len(parsersList) != 1:
        print('输入参数有误')
        return -1;
    if not currentUser.isLogin:
        print('请先登录')
        return -1;

    _mid = int(parsersList[0])
    # 判断留言是否存在
    res, _ = MessageBoardDB.request(
        f'select mid from messageInfo where mid={_mid}'
    )
    if res<1:
        return -1

    # 判断是否已经点赞过
    res, _ = MessageBoardDB.request(
        f'select mid from liked where mid={_mid} and uid={currentUser.uid}'
    )
    if res >= 1:
        print('点赞成功')
        return 0

    # 增加点赞记录
    res, _ = MessageBoardDB.request(
        f'insert into liked (mid,uid,likeDate) values ({_mid},{currentUser.uid},NOW())'
    )

    if updateLikedNum(_mid)<0:
        print('点赞失败')
        return -1
    else:
        print('点赞成功')
        return 0


@parser.addCmd("unlike_msg")
def unlike_msg(parsersList: List[str]):
    if len(parsersList) != 1:
        print('输入参数有误')
        return -1;
    if not currentUser.isLogin:
        print('请先登录')
        return -1;

    _mid = int(parsersList[0])

    res, _ = MessageBoardDB.request(
        f'delete from liked where mid={_mid} and uid={currentUser.uid}'
    )
    # 删除成功更新留言表
    if res > 0:
        updateLikedNum(_mid)

    return 0


if __name__ == '__main__':
    while not isExit:
        parser.parserCmd()
    print('Bye')

    pass
