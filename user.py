
class User:
    def __init__(self, username = '', nickname = 'anonymity'):
        self.username = username
        self.nickname=nickname
        self.uid=-1
        self.isLogin=False
        self.createDate=None

    def setUser(self,username, nickname, uid, createDate):
        self.username = username
        self.nickname = nickname
        self.uid = uid
        self.createDate = createDate
        self.isLogin = True

    def Logout(self):
        self.isLogin = False
