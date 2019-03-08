import socket
import _thread
import fcntl
import json
import time
import os


ip_port = ('0.0.0.0',10023)
fileinfoSep = ' '#文件中不能有这个符号 此为空格

def getUserList():
    userList = {}
    fileList = os.listdir()
    for f in fileList:
        if(os.path.isdir(f)):
            if '-' in f:
                userList[f.split('-')[0]] = f.split('-')[1]
    return userList


def login(conn, user):
    userFolder = conn.recv(1024).decode()
    (username,passwd) = userFolder.split('-') 
    if (username in user) and (passwd == user[username]):
        conn.send(b'1')
        return userFolder
    else:
        conn.send(b'0')
        return 0
    
def regist(conn, userList):
    nameRegist = conn.recv(1024).decode()
    if (nameRegist) and nameRegist in userList:
        reply = '1'
        conn.send(reply.encode())
    else:
        reply = '0'
        conn.send(reply.encode())
        passwd = conn.recv(1024).decode()
        userList[nameRegist] = passwd
        os.mkdir(nameRegist+'-'+passwd)
        conn.send(b'0')
    return int(reply),nameRegist



# ----------------------------------------------






def readAirList(airUserFolder):
    try:
        f = open(airUserFolder+os.sep+'.airFileList.txt','w')
        for root, dirs, files in os.walk(airUserFolder):
            for file in files:
                path = os.path.join(root, file)
                mtime = os.path.getmtime(path)
                filesize = os.path.getsize(path)
                fileinfo = '/'+path[len(airUserFolder)+1:]+fileinfoSep+str(mtime)+fileinfoSep+str(filesize)+'\n'
                f.write(fileinfo)
        print('read air list success')
        f.close()
        return 1
    except:
        print('read air list fail')
        return 0 #如果open失败，说明传过来的用户名密码是错误的，因为在注册时就创建了用户目录


def readOneFile(filePath):
    try:
        f = open(filePath, "rb")
        fcntl.flock(f.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
        data = f.read()
        f.close()# the same time we unlocks the file
        return data
    except:
        print("maybe some is using the target file |or| we cannot find %s file."%filePath)
        return 0


def getFileMD5(filePath):
    return hashlib.md5(open(filePath,'rb').read()).hexdigest()

def getFileInfo(filePath):
    filesize = os.path.getsize(filePath)
    modifyTime = os.path.getmtime(filePath)
    #md5 = getFileMD5(filePath)
    fileInfoHead = {
        #'filePath': filePath,
        'filesize': filesize,
        'modifyTime': modifyTime,
        #'md5': md5,
    }
    return json.dumps(fileInfoHead)


def sendOneFile(conn, airUserFolder):
    airFilePath = conn.recv(1024).decode()
    filePath = airUserFolder+airFilePath
    #filePath = airUserFolder+os.sep+airFilePath
    if(os.path.exists(filePath)):
        print('exits:\t\t',filePath)
        conn.send(b'1')

        fileInfoHead = getFileInfo(filePath)
        conn.send(fileInfoHead.encode())
        ack = conn.recv(7).decode()
        if ack == 'headAck':
            data = readOneFile(filePath)#data 返回为byte型
            conn.sendall(data)#在这里改断点续传
            flag = conn.recv(1).decode()
            if(flag=='1'):
               return 1
            else:
                print('flag receive error')
        elif ack == 'noneeds':
            return 0
    else:
        print('not exits:\t',filePath)
        conn.send(b'0')
        return 0


def getOneFile(airFilePath, writeFilePath, socket):
    if(os.sep in writeFilePath):
        if(not os.path.exists(writeFilePath.rsplit(os.sep,1)[0])):
            os.mkdir(writeFilePath.rsplit(os.sep,1)[0])

    socket.send(airFilePath.encode())

    hasFileFlag = socket.recv(1).decode()
    if(hasFileFlag == '1'):
        fileInfoHead = json.loads(socket.recv(4096))
        filesize = int(fileInfoHead['filesize'])
        remoteMtime = fileInfoHead['modifyTime']
        #airFilePath = fileInfoHead['filePath']

        if(os.path.isfile(writeFilePath)):
            localMtime = os.path.getmtime(writeFilePath)
            if(localMtime>remoteMtime):
                socket.send(b'noneeds')
                print("doesn't need to recv:\t\t",writeFilePath)
                return 0 
        #else:
        socket.send(b'headAck')
        with open(writeFilePath,'wb') as fp:
            while(filesize):
                data = socket.recv(4096)#data在send时是byte型的 因此此处不用decode(s) 且读时要wb读
                fp.write(data)
                lenRe = len(data)
                filesize = filesize - lenRe
        socket.send(b'1')
        print("Success write file:\t\t",writeFilePath)
        return 1

    elif(hasFileFlag == '0'):
        return 0

def listFileContent(localFolder):
    fileList = {}
    with open(localFolder, 'r') as f:
        for line in f.readlines():
            line=line.strip('\n')
            fileList[line.rsplit(fileinfoSep,2)[0]]=line.rsplit(fileinfoSep,2)[1]
    return fileList

def getNewer(socket, localFolder, airFolder):
    airFileList = listFileContent(localFolder+os.sep+'.airFileList.txt')
    localFileList = listFileContent(localFolder+os.sep+'.localFileList.txt')
    files = localFileList.copy() #copy深拷贝
    for i in airFileList:
        files[i] = airFileList[i]
        if i in localFileList:
            if(airFileList[i]<localFileList[i]):
                files[i] = localFileList[i]               
    numOfFile = str(len(files))
    socket.send(numOfFile.encode())
    re = socket.recv(3).decode()
    if(re == 'ack'):
        for file in files:
            localFilePath = localFolder+file
            #localFilePath = localFolder+os.sep+file
            #print(file,'12131231312')
            getOneFile(file, localFilePath, socket)








def control(conn,addr,user):
    print('\nsyn from ',addr)
    userChoice = conn.recv(1).decode()

    if userChoice == '0':
        flag,nameRegist = regist(conn, user)
        if(not flag):
            conn.close()
            print(nameRegist,"has registed and user folder has created")
            print(addr,'lost connect')
        else:
            conn.close()
            print(nameRegist,"registed error")
            print(addr,'lost connect')


    elif userChoice == '1':
        userFolder = login(conn, user)
        if(userFolder == 0):
            print("login fail")
        else:
            print(userFolder.split('-')[0],'login success')
        conn.close()
        print(addr,'lost connect')


    elif userChoice == 'L':
        airUserFolder = conn.recv(1024).decode()
        print('syn folder(air): ', airUserFolder)
        conn.send(b'ack')
        #userLocalFolder = conn.recv(1024).decode()
        #print('syn folder(user): ', userLocalFolder)
        #conn.send(b'ack')

        readAirList(airUserFolder)
        sendOneFile(conn, airUserFolder)#send air-list:

        conn.close()
        print(addr,'lost connect')


    elif userChoice == 'S':
        airUserFolder = conn.recv(1024).decode()
        print('syn folder(air): ', airUserFolder)
        conn.send(b'ack')
        userLocalFolder = conn.recv(1024).decode()
        print('syn folder(user): ', userLocalFolder)
        conn.send(b'ack')

        readAirList(airUserFolder)
        #send air-list:
        sendOneFile(conn, airUserFolder)# 每次调用期待一个请求 用try或者time out
        #get user-list:
        getOneFile('/.localFileList.txt', airUserFolder+os.sep+'.localFileList.txt', conn)
        
        #give newer:
        numOfFile = conn.recv(4096).decode()
        numOfFile = int(numOfFile)
        conn.send(b'ack')
        while(numOfFile!=0):
            sendOneFile(conn, airUserFolder)
            numOfFile = numOfFile - 1

        getNewer(conn, airUserFolder, userLocalFolder)

        conn.close()
        print(addr,'lost connect')





def main():
    user = getUserList()
    print("User list: ", user)

    serverSocket = socket.socket()
    serverSocket.bind(ip_port)
    serverSocket.listen(5)
    print('socket listen on ',ip_port[1],'\n')

    while True:
        try:
            conn, addr = serverSocket.accept()
            _thread.start_new_thread( control, (conn,addr,user,) )
        except:
           print("Error: unable to start thread")
           #return 0

if __name__ == '__main__':
    main()

