import Socket2Server
import os
#a= Socket2Server.regist('test3', 'test')
#a = Socket2Server.login('test', 'test')
#print(a)
#type(a) = int

# dictt = Socket2Server.giveGuiAirList()
# print(dictt)

# a = Socket2Server.synAll('yygshezhi')
# print(a)

# folderPath = '/10'
# folderInfo = Socket2Server.giveGuiFolderChild(folderPath)
# print(folderInfo)

name = '/DSA.md'
fileInfo = Socket2Server.giveGuiOneFileInfo(name)
print(fileInfo)





#注意：
# token.cookie是 byte模式写入 避免了间隔符导致的密码写入读取失败。

# 返回值列表：
# a=0 token写入失败 
# a=5 tcp错误
# a=1 注册成功
# a=2 注册名字被占用
# a=3 登陆成功
# a=4 登陆错误
# a=5 tcp错误
#-------
# a=6 token读取失败
# username,password = C.giveGuiUserName()
# print(username,password)



# 测试：

# $ cd "/Users/yuanyige/Library/Mobile Documents/com~apple~CloudDocs/Work/syn_201811211814/fileSYNserver"
# $ python3 S.py

# 跑在后台看到有 listen 即可


# getlist 需要修改，需要有返回值判断是失败还是空文件
# return 5 tcp
# ret.   8 fail
