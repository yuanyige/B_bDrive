import socket
import json
import time
import sys
import os
#import re

#ip_port = ('192.168.1.102',10023)
ip_port = ('127.0.0.1',10023)

fileinfoSep = ' '#文件中不能有这个符号 此为空格



def readlocalList(localFolder):
    if(not os.path.exists(localFolder)):
        os.mkdir(localFolder)
    try: 
        f = open(localFolder+os.sep+'.localFileList.txt','w')
        for root, dirs, files in os.walk(localFolder):
            for file in files:
                path = os.path.join(root, file)
                mtime = os.path.getmtime(path)               
                fileinfo = '/'+path[len(localFolder)+1:]+fileinfoSep+str(mtime)+'\n'
                f.write(fileinfo)
        print("read local file list success")
        f.close()
        return 1
    except:
        print("read local file list fail")
        return 0
    


def readOneFile(filePath):
    try:
        f = open(filePath, "rb")
        data = f.read()
        f.close()
        return data
    except:
        print("[Error]: cannot find %s file."%filePath)
        return 0


def getFileInfo(filePath):
    filesize = os.path.getsize(filePath)
    modifyTime = os.path.getmtime(filePath)
    #md5
    fileInfoHead = {
        #'filePath': filePath,
        'filesize': filesize,
        'modifyTime': modifyTime,
    }
    return json.dumps(fileInfoHead)


def sendOneFile(conn, localFolder):
    airFilePath = conn.recv(1024).decode()
    #filePath = localFolder+os.sep+airFilePath
    filePath = localFolder+airFilePath
    if(os.path.exists(filePath)):
        print('exits:\t\t',filePath)
        conn.send(b'1')

        fileInfoHead = getFileInfo(filePath)
        conn.send(fileInfoHead.encode())
        ack = conn.recv(7).decode()
        if ack == 'headAck':
            data = readOneFile(filePath)
            conn.sendall(data)#在这里改断点续传
            flag = conn.recv(1).decode()
            if(flag):
                return 1
        elif ack == 'noneeds':
            return 0
    else:
        print('not exits:\t',filePath)
        conn.send(b'0')
        return 0


def getAirList(username, password, localFolder):
    try:
        conn = socket.socket()
        conn.connect(ip_port)
    except:
        return 5 #tcp error
    
    conn.send(b'L')

    airFolder = username + '-' + password

    conn.send(airFolder.encode())
    if(conn.recv(3).decode() == 'ack'):
        getOneFile('/.airFileList.txt', localFolder+os.sep+'.airFileList.txt', conn)
    conn.close()
    airFileList = listFileContent(localFolder+os.sep+'.airFileList.txt')
    return airFileList


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
        socket.send(b'headAck')
        with open(writeFilePath,'wb') as fp:
            while(filesize):
                data = socket.recv(4096)#.decode()
                fp.write(data)
                lenRe = len(data)
                filesize = filesize - lenRe
        socket.send(b'1')
        #print("Success write file:\t\t",writeFilePath)
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

    files = localFileList
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
            getOneFile(file, localFilePath, socket)



#####################################################################

#synAll(username, password, localFolder)
def synAll(localFolder):#username, password, 
    username,password = giveGuiUserName()
    try:
        conn = socket.socket()
        conn.connect(ip_port)
    except:
        print(5) #tcp error

    airFolder = username + '-' + password
    localFolder = localFolder

    conn.send(b'S')
    conn.send(airFolder.encode())
    if(conn.recv(3).decode() == 'ack'):
        conn.send(localFolder.encode())
        if(conn.recv(3).decode() == 'ack'):
            readlocalList(localFolder)

            getOneFile('/.airFileList.txt', localFolder+os.sep+'.airFileList.txt', conn)
            sendOneFile(conn, localFolder)#send local file list

            getNewer(conn, localFolder, airFolder)

            #upload all
            numOfFile = conn.recv(4096).decode()
            numOfFile = int(numOfFile)
            conn.send(b'ack')
            while(numOfFile!=0):
                sendOneFile(conn, localFolder)
                numOfFile = numOfFile - 1
            return 1
    conn.close()



def login(username, password):
    try:
        clientSocket = socket.socket()
        clientSocket.connect(ip_port)
    except:
        return 5 #tcp error
    clientSocket.send(b'1')#model = login
    airFolerPath = username+"-"+password
    clientSocket.send(airFolerPath.encode())
    flag = clientSocket.recv(1).decode()
    if(flag == '1'):
        try:
            if(not os.path.exists('temp')):
                os.mkdir('temp')
            fp = open('temp/token.cookie','wb')
            fp.write(username.encode()+b'\n'+password.encode())
            fp.close()#login success
            return 3
        except:
            return 0 #token写入失败
        return 3
    if(flag == '0'):
        return 4#fail


def regist(username,password):
    try:
        clientSocket = socket.socket()
        clientSocket.connect(ip_port)
    except:
        return 5#print('tcp error')
    clientSocket.send(b'0')#model = regist
    clientSocket.send(username.encode())
    reply = clientSocket.recv(1).decode()

    if(reply == '1'):
        clientSocket.close()
        return 2#print("name used")

    elif(reply == '0'):
        clientSocket.send(password.encode())
        reply = clientSocket.recv(1).decode()
        if(reply == '0'):
            clientSocket.close()
            return 1
        else:
            return 5#print("tcp error")


def giveGuiUserName():
    try:
        fp = open('temp/token.cookie','rb')
        a = fp.read()
        username,password = a.split(b'\n',1)
        return username.decode(), password.decode()
    except:
        return 0


def giveGuiAirList():
    try:
        fp = open('temp/token.cookie','rb')
        a = fp.read()
        username,password = a.split(b'\n',1)
        infoDic = getAirList(username.decode(), password.decode(), 'temp')
        print(infoDic)
        fileList = [key for key in infoDic.keys()]
        fileList.remove('.localFileList.txt')
        fileList.remove('.airFileList.txt')
        fileList.remove('.DS_Store')
        return fileList
    except:
        return 0


def giveGuiFolderChild(folderPath):#
    try:
        fp = open('temp/token.cookie','rb')
        a = fp.read()
        username,password = a.split(b'\n',1)
        infoDic = getAirList(username.decode(), password.decode(), 'temp')
        folderChild = []
        for i in infoDic:
            if i.startswith(folderPath):
                temp = i.lstrip(folderPath)
                #print(temp,'-----')
                if '.DS_Store' in temp or '.localFileList.txt' in temp or '.airFileList.txt' in temp :
                    pass
                elif os.sep in temp:
                    temp = temp.split(os.sep)[0] + '/'
                    temp = i.split(temp)[0]+temp
                    if temp in folderChild:
                        pass
                    else:
                        folderChild.append(temp)
                else:
                    folderChild.append(i)
        return folderChild
    except:
        return 0



def giveGuiOneFileInfo(fileName):
    try:
        with open('temp'+os.sep+'.airFileList.txt', 'r') as f:
            for line in f.readlines():
                line=line.strip('\n')
                if fileName in line:
                    oneFileInfo = []
                    line = line.rsplit(fileinfoSep,2)
                    mtime = time.localtime(float(line[1]))
                    mtime = str(time.strftime("%Y-%m-%d %H:%M:%S", mtime) )
                    oneFileInfo.append(mtime)
                    size = int(line[2])/1024
                    oneFileInfo.append(str(size))
                    print(oneFileInfo)
                    return oneFileInfo
    except:
        return 0

