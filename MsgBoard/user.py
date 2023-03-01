from typing import List

class User:
    def __init__(self, MessageBoardDB, username = '', nickname = 'anonymity'):
        self.MessageBoardDB = MessageBoardDB
        self.username = username
        self.nickname=nickname
        self.uid=-1
        self.isLogin=False
        self.createDate=None
        self.msgList = set()
        self.likedList = set()

    # 获取当前用户的留言
    def getUserMsg(self):
        res, data = self.MessageBoardDB.request(
            f'select mid from messageInfo where uid={self.uid}'
        )
        for v in data:
            self.msgList.add(v['mid'])

    def getUserLiked(self):
        res, data = self.MessageBoardDB.request(
            f'select mid  from liked where uid="{self.uid}"'
        )
        for v in data:
            self.likedList.add(v['mid'])

    def logout(self):
        self.isLogin = False

    def login(self, parsersList: List[str]):
        if len(parsersList) != 2:
            print('输入参数有误')
            return -1;

        if self.isLogin:
            print('已经有用户登录了')
            return -1;

        res, data = self.MessageBoardDB.request(
            f'select *  from users where username="{parsersList[0]}" and password = "{parsersList[1]}"'
        )

        if res >= 1:
            data = data[0]
            self.username=data['username']
            self.nickname=data['nickname']
            self.uid=data['uid']
            self.createDate=data['createDate']
            self.isLogin = True

            self.getUserMsg()
            self.getUserLiked()
            print('登录成功')
        else:
            print('登录失败')
        return 0

    def logon(self, parsersList: List[str]):
        if len(parsersList) != 3:
            print('输入参数有误')
            return -1;

        res, _ = self.MessageBoardDB.request(
            f'insert into users(username,nickname,password,createDate) '
            f'values("{parsersList[0]}","{parsersList[1]}","{parsersList[2]}",NOW())'
        )

        if res == 1:
            print('注册成功')
        else:
            print('注册失败')
        return 0