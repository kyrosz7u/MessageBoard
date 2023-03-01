from typing import List
import time, threading, copy


class Likemsg:
    def __init__(self, user, MessageBoardDB):
        self.currentUser = user
        self.MessageBoardDB = MessageBoardDB
        self.OpBuffer = []
        self.isMainLoopExit = False
        self.asyncThread = threading.Thread(target=self.threadFunc)
        self.asyncThread.start()
        self.bufferLock = threading.Lock()

    def exit(self):
        self.isMainLoopExit = True
        self.asyncThread.join()

    def updateLikedNum(self, midList):
        # 查询该留言的点赞人数
        _likedNum = []
        for _mid in midList:
            res, data = self.MessageBoardDB.request(
                f'select count(uid) from liked where mid={_mid}'
            )
            _likedNum.append(data[0]['count(uid)'])

        for i in range(0,len(midList)):
            # 更新点赞人数
            res, _ = self.MessageBoardDB.request(
                f'update messageInfo set likedNum={_likedNum[i]} where mid={midList[i]}'
            )


    def like_msg(self, parsersList: List[str]):
        if len(parsersList) != 1:
            print('输入参数有误')
            return -1;
        if not self.currentUser.isLogin:
            print('请先登录')
            return -1;

        _mid = int(parsersList[0])

        # 判断是否已经点赞过
        if _mid in self.currentUser.likedList:
            print('已经点赞过了')
            return 0
        # 增加点赞记录
        else:
            self.bufferLock.acquire()
            self.OpBuffer.append({'add': _mid})
            self.bufferLock.release()
            self.currentUser.likedList.add(_mid)
            print('点赞成功')

    def unlike_msg(self, parsersList: List[str]):
        if len(parsersList) != 1:
            print('输入参数有误')
            return -1;
        if not self.currentUser.isLogin:
            print('请先登录')
            return -1;

        _mid = int(parsersList[0])

        if _mid in self.currentUser.likedList:
            self.bufferLock.acquire()
            self.OpBuffer.append({'del': _mid})
            self.bufferLock.release()
            self.currentUser.likedList.remove(_mid)
            print('取消点赞成功')

        else:
            print('没有点赞过该条留言')
            return -1

    def flush_to_db(self):
        if len(self.OpBuffer) < 1:
            return

        self.bufferLock.acquire()
        opList = copy.deepcopy(self.OpBuffer)
        self.OpBuffer = []
        self.bufferLock.release()

        addList = []
        delList = []
        # 将buffer中的操作分类
        for v in opList:
            if 'add' in v:
                addList.append(v['add'])
            elif 'del' in v:
                delList.append(v['del'])

        # 合并请求
        addSqlStr=''
        for v in addList:
            addSqlStr+=f'({v},{self.currentUser.uid},NOW()),'
        if addSqlStr != '':
            # 去掉末尾的','
            addSqlStr = addSqlStr[:-1]
            res, _ = self.MessageBoardDB.request(
                f'insert into liked (mid,uid,likeDate) values '+addSqlStr
            )

        delSqlStr = ''
        for v in delList:
            delSqlStr += f'({v},'
        if delSqlStr != '':
            delSqlStr = delSqlStr[:-1]
            delSqlStr+=')'
            res, _ = self.MessageBoardDB.request(
                f'delete from liked where mid in {delSqlStr} and uid={self.currentUser.uid}'
            )

        self.updateLikedNum(addList+delList)


    def threadFunc(self):
        while not self.isMainLoopExit:
            time.sleep(1)
            self.flush_to_db()

