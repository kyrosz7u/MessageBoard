from typing import List
import IPython

class Comment:
    def __init__(self, user, MessageBoardDB):
        self.currentUser = user
        self.MessageBoardDB = MessageBoardDB

    def add_msg(self, parsersList: List[str]):
        if not self.currentUser.isLogin:
            print('请先登录')
            return -1;

        # parsersList中保存了按空格拆分的留言info
        # 需要恢复原来的内容
        msgStr = ''
        for i in range(len(parsersList)-1):
            msgStr += parsersList[i]+' '
        msgStr += parsersList[-1]

        res, data = self.MessageBoardDB.request(
            f'insert into messageInfo (uid,nickname,likedNum,messageDate,info) '
            f'values ("{self.currentUser.uid}","{self.currentUser.nickname}",0,NOW(),"{msgStr}")'
        )
        res, data = self.MessageBoardDB.request('SELECT LAST_INSERT_ID()')
        self.currentUser.msgList.add(data[0]['LAST_INSERT_ID()'])
        print('留言成功')

    def del_msg(self, parsersList: List[str]):
        if len(parsersList) != 1:
            print('输入参数有误')
            return -1;
        _mid = int(parsersList[0])

        if _mid not in self.currentUser.msgList:
            print('删除失败')
            return -1
        else:
            res, data = self.MessageBoardDB.request(
                f'delete from messageInfo where mid={_mid}'
            )
            self.currentUser.msgList.remove(_mid)
            print('删除成功')
            return 0

