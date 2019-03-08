import sys
import Socket2Server
from lib.ItemClasses import *
from lib.WindowFrame import QUnFrameWindow
from functools import partial
from PyQt5.QtCore import Qt,QRectF
from PyQt5.QtGui import QIcon,QPainter,QBrush,QColor,QLinearGradient,QFont
from PyQt5.QtCore import QTimer


class FileSynWindow (QUnFrameWindow):
	def __init__(self):
		super(FileSynWindow, self).__init__()
		self.setCloseButton(True)
		self.setStyleSheet("QTitleButton#CloseButton:hover{border-top-right-radius: 5px;}")
		self.setMinButton(True)
		self.setMaxButton(True)
		self.setGeometry(280,150,800,500)
		self.fileButtonList=[]
		self.fileLabelList=[]
		self.initUI()

	def paintEvent(self, ev):
		painter = QPainter(self)
		painter.setBrush(QBrush(QColor(50,50,50,240)));
		painter.setPen(QColor(255,255,255,150));
		painter.setRenderHint(QPainter.Antialiasing)
		gradient = QLinearGradient(QRectF(self.rect()).topLeft(),QRectF(self.rect()).bottomLeft())
		painter.drawRoundedRect(self.rect(),5, 5)
		painter.end()


	def initUI(self):
		'''
		初始化左方菜单栏界面
		'''
		self.menuSpace=QBorderWidget()
		self.menuSpace.color=QColor(255,255,255,25)
		self.menuSpace.setMinimumSize(150, 200)
		self.initMenuSpace()


		'''
		创建右方栈切换控件
		'''
		self.spaceStack=QStackedWidget(self)


		'''
		初始化右方切换栈--全文件界面
		并与菜单栏控件进行信号连接
		'''
		self.allFileSpace=QBorderWidget()
		self.allFileSpace.color=QColor(0,0,0,160)
		self.allFileSpace.setMinimumSize(791, 425)
		self.allFileSpace.setObjectName("FileSpace")
		self.allFileScroll = QScrollArea(self)
		self.allFileScroll.setWidget(self.allFileSpace)
		self.toolBar=QBorderWidget()
		self.toolBar.color=QColor(0,0,0,50)
		self.toolBar.setMinimumSize(150,30)
		tmpL=QVBoxLayout()
		tmpL.addWidget(self.toolBar)
		tmpL.addWidget(self.allFileScroll)
		tmpL.setContentsMargins(0,0,1,0)
		tmpL.setSpacing(0)
		tmpW=QWidget()
		tmpW.setLayout(tmpL)
		self.spaceStack.addWidget(tmpW)
		self.initAllFileSpace()
		self.allFileButton.clicked.connect(lambda:self.spaceStack.setCurrentIndex(0))


		'''
		初始化右方切换栈--正在下载界面
		并与菜单栏控件进行信号连接
		'''
		self.dowSpace=QWidget()
		self.dowSpace.setObjectName("RSpace")
		self.spaceStack.addWidget(self.dowSpace)
		self.dowButton.clicked.connect(lambda:self.spaceStack.setCurrentIndex(1))


		'''
		创建分割控件分割左右空间
		左为菜单空间，右为栈切换空间
		'''
		self.splitter = QSplitter(Qt.Horizontal)
		self.splitter.addWidget(self.menuSpace)
		self.splitter.addWidget(self.spaceStack)
		self.splitter.setStretchFactor(0,150)
		self.splitter.setStretchFactor(1,650)


		'''
		创建整体垂直布局控件
		将顶部、分割器、底部加入布局
		'''
		self.mainLayout=QVBoxLayout(self)
		self.mainLayout.addWidget(self._TitleLabel)
		self._TitleLabel.setFixedSize(800,15)
		self.mainLayout.addWidget(self.splitter)
		self.frame=QFrame()
		self.frame.setFixedSize(800,0.5)
		self.mainLayout.addWidget(self.frame)
		self.mainLayout.setContentsMargins(1,10,0,10)
		self.mainLayout.setSpacing(5)


		'''
		初始化定时器
		用来显示显示器文本
		'''
		self.timer = QTimer(self) 
		self.timer.timeout.connect(self.TextDisplay)
		self.timer.start(5000) 




	def initMenuSpace(self):
		'''
		左方菜单栏界面具体初始化
		'''
		menuLayout=QVBoxLayout(self.menuSpace)
		menuLayout.setContentsMargins(0,0,0,0)
		menuLayout.setSpacing(0)

		self.display=QLabel(self.menuSpace)
		self.display.setObjectName("Display")
		self.display.resize(150,75)
		self.display.setFrameStyle(QFrame.Box | QFrame.Plain)
		self.display.setAlignment(Qt.AlignCenter)
		#self.display.setFont(QFont("Timers", 15 ,QFont.Bold))

		menuLayout.addStretch(20)
		self.allFileButton=QMenuButton()
		self.allFileButton.setObjectName("MenuButton")
		self.allFileButton.setText("全部文件")
		self.allFileButton.setFixedSize(150,60)
		self.allFileButton.move(0,40)
		menuLayout.addWidget(self.allFileButton)
		menuLayout.addStretch(1)

		self.dowButton=QMenuButton()
		self.dowButton.setObjectName("MenuButton")
		self.dowButton.setText("正在下载")
		self.dowButton.setFixedSize(150,60)
		self.dowButton.move(0,100)
		menuLayout.addWidget(self.dowButton)
		menuLayout.addStretch(1)

		self.upButton=QMenuButton()
		self.upButton.setObjectName("MenuButton")
		self.upButton.setText("正在上传")
		self.upButton.setFixedSize(150,60)
		self.upButton.move(0,160)
		menuLayout.addWidget(self.upButton)
		menuLayout.addStretch(1)

		self.sucButton=QMenuButton()
		self.sucButton.setObjectName("MenuButton")
		self.sucButton.setText("传输完成")
		self.sucButton.setFixedSize(150,60)
		self.sucButton.move(0,220)
		menuLayout.addWidget(self.sucButton)
		menuLayout.addStretch(40)

		self.synButton=QButton(self.menuSpace)
		self.synButton.setObjectName("SynButton")
		self.synButton.setFixedSize(70,20)
		self.synButton.setText("同步")
		self.synButton.move(42,350)

		self.logoutButton=QButton(self.menuSpace)
		self.logoutButton.setObjectName("LogoutButton")
		self.logoutButton.setFixedSize(70,20)
		self.logoutButton.setText("注销")
		self.logoutButton.move(42,400)

		self.logoutButton.clicked.connect(self.Back2Login)
		self.synButton.clicked.connect(self.SynFile)


	def initAllFileSpace(self):
		'''
		右方全文件界面的初始化
		'''
		self.route=['/']
		fileList=self.GetFileList()
		ret=self.ShowFileList(fileList)
		if ret:
			self.display.setText("服务器状态良好\n已呈现云端文件")
		
		self.backButton=QButton(self.toolBar)
		self.backButton.setObjectName("DirBackButton")
		self.backButton.setFixedSize(23,23)
		self.backButton.move(10,3)
		self.backButton.clicked.connect(self.BackFolder) 
		self.backButton.setIcon(QIcon("img/back.png"))
		self.backButton.setEnabled(False)

		self.freshButton=QButton(self.toolBar)
		self.freshButton.setObjectName("RefreshButton")
		self.freshButton.setFixedSize(23,23)
		self.freshButton.move(40,3)
		self.freshButton.clicked.connect(self.Refresh)
		self.freshButton.setIcon(QIcon("img/refresh.png"))

		self.helpButton=QButton(self.toolBar)
		self.helpButton.setObjectName("HelpButton")
		self.helpButton.setFixedSize(23,23)
		self.helpButton.move(70,3)
		self.helpButton.setIcon(QIcon("img/help.png"))

		self.searchLabel=QLabel(self.toolBar)
		self.searchLabel.setObjectName("SearchLabel")
		self.searchLabel.setFixedSize(18,18)
		self.searchLabel.move(102,6)

		self.dirInput=QTextInput(self.toolBar)
		self.dirInput.setObjectName("DirInput")
		self.dirInput.setPlaceholderText("请输入路径")
		self.dirInput.setAlignment (Qt.AlignCenter)
		self.dirInput.setFixedSize(120,23)
		self.dirInput.move(100,3)
		self.dirInput.returnPressed.connect(self.GoToPath)



####################################### 以下为功能函数 #######################################


	def GetFileList(self):
		'''
		从服务器请求顶层文件列表
		'''
		Flist = Socket2Server.giveGuiFolderChild(self.route[0])
		return Flist


	def ShowFileList(self,fileList):
		'''
		界面化展示文件列表
		'''
		if fileList:
			self.display.setText("当前目录\n"+str(self.route[-1]))
			self.allFileSpace.setMinimumSize(750, max(len(fileList)*24,425))
			if self.fileButtonList and self.fileLabelList:
				for i in self.fileButtonList:
					i.deleteLater()
				for j in self.fileLabelList:
					j.deleteLater()
				self.fileButtonList=[]
				self.fileLabelList=[]
			for i in fileList:
				index=fileList.index(i)
				# Button
				self.FileButton=QFileButton(self.allFileSpace)
				self.FileButton.name=i
				self.fileButtonList.append(self.FileButton)
				self.FileButton.setFixedSize(70,70)
				#suffix=i.split(".")
				if i[-1]=="/":
					suffix="Folder"
				elif len(i.split("."))>1:
					suffix=i.split(".")[1]
				else:
					suffix="Null"
				self.FileButton.setStyleSheet("QFileButton{background-image:url(./img/"+suffix+".png);background-color:rgba(0,0,0,0);}QFileButton:hover{background-image:url(./img/"+suffix+"_h.png);background-color:rgba(0,0,0,0);}")
				self.FileButton.move(40+(index%6)*120,60+(index//6)*110)
				self.FileButton.show()
				# Label
				self.FileLabel=QTextLabel(self.allFileSpace)
				tmpT1=i.split("/")[-1] if i.split("/")[-1]!="" else i.split("/")[-2]
				tmpT2=tmpT1.split(".")[-1] if len(tmpT1.split("."))==1 else tmpT1.split(".")[-2]
				self.FileLabel.setText(tmpT2 if len(tmpT2)<=6 else tmpT2[0:6]+"..")
				self.fileLabelList.append(self.FileLabel)
				self.FileLabel.setFixedSize(70,20)
				self.FileLabel.move(40+(index%6)*120,130+(index//6)*110)
				self.FileLabel.setObjectName("FileLabel")
				self.FileLabel.setAlignment(Qt.AlignCenter)
				self.FileLabel.show()
				# 设置鼠标悬浮信息提示
				fileInfo=Socket2Server.giveGuiOneFileInfo(i)
				if fileInfo:
					self.FileButton.setToolTip("文件名:"+tmpT1+"\n文件路径:"+i+"\n文件大小:"+str(fileInfo[1])[0:6]+"KB  \n最后修改时间:"+str(fileInfo[0]))

			# 设置文件夹按钮点击事件
			for i in range(len(self.fileButtonList)):
				self.fileButtonList[i].clicked.connect(partial(self.IntoFolder,self.fileButtonList[i].name))
			return 1
		else:
			self.display.setText("服务器状态异常\n请检查以获得服务")
			return 0



	def IntoFolder(self,filePath):
		#print("点击了:",filePath)
		'''
		请求服务器某目录下层文件列表
		并显示该目录内容，即进入该下层目录
		'''
		if filePath[-1]=="/": # 判断是目录，不是普通文件
			self.route.append(filePath)
			subList = Socket2Server.giveGuiFolderChild(filePath)
			ret=self.ShowFileList(subList)
			if ret:
				self.backButton.setEnabled(True)
				self.display.setText("当前目录\n"+str(self.route[-1]))
		else:
			self.display.setText("鼠标悬停即可\n获得文件信息")


	def BackFolder(self):
		'''
		维护路径表记录进入文件夹的路径
		请求服务器某目录上层文件列表
		并显示该目录内容，即进入该上层目录
		'''
		parentPath=self.route[-1].rsplit("/",2)[0]+"/"
		# print("返回的上级目录",parentPath)
		parentList=Socket2Server.giveGuiFolderChild(parentPath)
		if parentPath =="/":
			self.backButton.setEnabled(False)
		ret=self.ShowFileList(parentList)
		if ret:
			self.route.pop()
			self.display.setText("当前目录\n"+str(self.route[-1]))


	def GoToPath(self):
		'''
		在输入框输入地址
		直接进入该目录
		'''
		path=self.dirInput.text()
		self.route.append(path)
		List=Socket2Server.giveGuiFolderChild(path)
		ret=self.ShowFileList(List)
		if ret:
			self.backButton.setEnabled(True)
			self.display.setText("当前目录\n"+str(self.route[-1]))


	def Refresh(self):
		'''
		更新按钮的功能定义
		获取一遍时时列表后展现在全文见目录
		'''
		List=Socket2Server.giveGuiFolderChild(self.route[-1])
		#self.FileButton.setStyleSheet("QFileButton{background-image:url(./img/5.png);}")
		ret=self.ShowFileList(List)
		if ret:
			self.display.setText("云端文件已更新")


	def SynFile(self):
		'''
		同步按钮的功能定义
		下载所有服务器文件后更新界面
		'''
		path = QFileDialog.getExistingDirectory(self)
		if path:
			print(path)
			Socket2Server.synAll(path)
			self.Refresh()
			self.display.setText("云端文件已同步")
		else:
			self.display.setText("文件同步已取消")


	def Back2Login(self):
		'''
		注销按钮的功能定义
		回退到登录界面
		'''
		from Login import LoginWindow
		window_login=LoginWindow()
		window_login.show()
		self.close()


	def TextDisplay(self):
		self.display.setText("网络程序设计\n课程大作业")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyleSheet(open("./lib/Style.qss").read())
	window_filesyn = FileSynWindow()
	window_filesyn.show()
	sys.exit(app.exec_())



