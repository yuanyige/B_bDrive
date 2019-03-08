import sys
import os
import Socket2Server
from lib.WindowFrame import QUnFrameWindow
from lib.ItemClasses import *
from FileSyn import FileSynWindow
from Login import LoginWindow  


class SignupWindow(QUnFrameWindow):
	def __init__(self):
		super(SignupWindow, self).__init__()
		self.setGeometry(500,250,300,300)
		self.setMaxButton(False)
		self.setCloseButton(True)
		self.setMinButton(True)
		self.initUI()
		self._SignupButton.clicked.connect(self.UserSignup)
		self._BackButton.clicked.connect(self.Back2Login)

	def initUI(self):
		# 安放文本输入框
		self._UsernameInput=QTextInput(self)
		self._PasswordInput=QTextInput(self)
		self._PasswordInputAgain=QTextInput(self)
		self._UsernameInput.setGeometry(65, 100, 170,30)
		self._UsernameInput.setPlaceholderText("请输入用户名")
		self._PasswordInput.setGeometry(65, 150, 170,30)
		self._PasswordInput.setPlaceholderText("请输入密码")
		self._PasswordInputAgain.setGeometry(65, 200, 170,30)
		self._PasswordInputAgain.setPlaceholderText("请再次输入密码")
		# 安放按钮
		self._SignupButton=QButton(self)
		self._SignupButton.setObjectName("SignupButton")
		self._SignupButton.setText("注册")
		self._SignupButton.setGeometry(170,260,70,20)
		self._BackButton=QButton(self)
		self._BackButton.setObjectName("BackButton")
		self._BackButton.setText("返回")
		self._BackButton.setGeometry(65,260,70,20)
		# 注册标签
		self._WelcomeLabel=QTextLabel(self)
		self._WelcomeLabel.setGeometry(110,40,100,20)
		self._WelcomeLabel.setText("欢迎注册")
		self._WelcomeLabel.setObjectName("WelcomeLabel")

		## 分界线
		self._LineLabel=QTextLabel(self)
		self._LineLabel.setGeometry(0,65,300,20)
		self._LineLabel.setText("————————————————————————————————————")
		self._LineLabel.setObjectName("LineLabel")


	def Back2Login(self):
		window_login=LoginWindow()
		window_login.show()
		self.close()

	def UserSignup(self):
		signup_user = self._UsernameInput.text()
		signup_password = self._PasswordInput.text()
		signup_password_2 = self._PasswordInputAgain.text()
		if signup_password_2 == signup_password:
			ret=Socket2Server.regist(signup_user,signup_password)
			if ret == 1:
				print("注册成功，清登录")	
				window_login=LoginWindow()
				window_login.show()
				self.close()
			elif ret == 2:
				print("用户名被占用，请重新输入")
			elif ret == 5:
				print("TCP错误,请重新登录")
		else:
			print("两次密码不一致，请重新输入")
		self._UsernameInput.setFocus()


if __name__ == "__main__": 

	app = QApplication(sys.argv)
	app.setStyleSheet(open("./lib/Style.qss").read())
	window_signup = SignupWindow()	
	window_signup.show()
	sys.exit(app.exec_())
