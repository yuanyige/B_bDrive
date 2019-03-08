import sys
import os
import Socket2Server
from lib.ItemClasses import *
from lib.WindowFrame import QUnFrameWindow
from lib.SwitchBtn import SwitchBtn



class LoginWindow(QUnFrameWindow):
	def __init__(self):
		super(LoginWindow, self).__init__()
		self.setGeometry(500,250,300,260)
		self.setMaxButton(False)
		self.setCloseButton(True)
		self.setMinButton(True)
		self.initUI()
		self._RemCtButton.checkedChanged.connect(self.RememberCt)
		self._LoginButton.clicked.connect(self.CheckUserLicense)
		self._SignupButton.clicked.connect(self.UserSignup)

	def initUI(self):
		# 安放文本输入框
		self._UsernameInput=QTextInput(self)
		self._PasswordInput=QTextInput(self)
		self._UsernameInput.setGeometry(65, 100, 170,30)
		self._UsernameInput.setPlaceholderText("请输入用户名")
		self._PasswordInput.setGeometry(65, 140, 170,30)
		self._PasswordInput.setEchoMode (2)
		self._PasswordInput.setPlaceholderText("请输入密码")
		# 安放按钮
		self._LoginButton=QButton(self)
		self._LoginButton.setObjectName("LoginButton")
		self._LoginButton.setText("登录")
		self._LoginButton.setGeometry(170,220,70,20)
		self._SignupButton=QButton(self)
		self._SignupButton.setObjectName("SignupButton")
		self._SignupButton.setText("注册")
		self._SignupButton.setGeometry(65,220,70,20)
		# 欢迎标签
		self._WelcomeLabel=QTextLabel(self)
		self._WelcomeLabel.setGeometry(110,40,100,20)
		self._WelcomeLabel.setText("欢迎登录")
		self._WelcomeLabel.setObjectName("WelcomeLabel")
		# 记住账号
		self._RemCtLabel=QTextLabel(self)
		self._RemCtLabel.setGeometry(65,185,100,20)
		self._RemCtLabel.setText("记住账号")
		self._RemCtLabel.setObjectName("RemCtLabel")
		self._RemCtButton=SwitchBtn(self)
		self._RemCtButton.setGeometry(120,187,30,15)
		# 忘记密码
		self._FgPwLabel=QTextLabel(self)
		self._FgPwLabel.setGeometry(180,185,100,20)
		self._FgPwLabel.setText("忘记密码?")
		self._FgPwLabel.setObjectName("FgPwLabel")
		## 分界线
		self._LineLabel=QTextLabel(self)
		self._LineLabel.setGeometry(0,65,300,20)
		self._LineLabel.setText("————————————————————————————————————")
		self._LineLabel.setObjectName("LineLabel")
	
	def UserSignup(self):
		from Signup import SignupWindow
		print("signup now")
		window_signup=SignupWindow()
		window_signup.show()
		self.close()		
	
	def CheckUserLicense(self):
		login_user = self._UsernameInput.text()
		login_password = self._PasswordInput.text()
		ret=Socket2Server.login(login_user,login_password)

		if ret == 3:
			print("login success")
			from FileSyn import FileSynWindow
			window_filesyn=FileSynWindow()
			window_filesyn.show()
			self.close()
		elif ret == 4:
			print("用户名或密码错误,请重新登录")							
		elif ret == 5:
			print("TCP错误,请重新登录")
		self._UsernameInput.setFocus()

	def RememberCt(self,checked):
		print(checked)
		if checked :
			rem_user=self._UsernameInput.text()
			rem_pwd=self._PasswordInput.text()
			#rem_file=open("userpwd.txt","a+")
			#rem_file.write(rem_user+","+rem_pwd)
			self._RemCtLabel.setStyleSheet("QTextLabel#RemCtLabel{color:rgba(100,184, 255,200);}")
		else:
			self._RemCtLabel.setStyleSheet("QTextLabel#RemCtLabel{color:rgba(255,255,255,150);}")
			


if __name__ == "__main__":    
	app = QApplication(sys.argv)
	app.setStyleSheet(open("./lib/Style.qss").read())
	window_login = LoginWindow()	
	window_login.show()
	sys.exit(app.exec_())
