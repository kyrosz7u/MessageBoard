# 留言系统
基于Python3.9环境+MySql8.0.31搭建
## 基本功能
1. 账号管理

    包括账号创建和登录，昵称支持中文，账号名与昵称支持重复校验。
2. 留言查看
    
    能够分页显示留言内容、留言人、点赞数，按照点赞数排行
3. 留言管理

    增加、删除留言，点赞和取消点赞，删除留言时会进行权限检查
## 控制台交互指令
```commandline
login <username> <password> - 登录账号
logon <username> <password> <nickname> - 创建账号
logoff - 退出登录
list [n] - 查看留言版，n表示查看第几页。如果省略n显示第一页。
add_msg <content> - 增加留言
del_msg <msg_id> - 删除留言
like_msg <msg_id> - 点赞留言
unlike_msg <msg_id> - 取消点赞
```