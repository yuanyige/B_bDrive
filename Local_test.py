from Login import LoginWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import re

pid=os.fork()
if pid:
	app = QApplication(sys.argv)
	app.setStyleSheet(open("./lib/Style.qss").read())
	window = LoginWindow()	
	window.show()
	sys.exit(app.exec_())

else:
	a=os.popen("lsof -i:10023")
	tmp=a.read().replace(" ","")

	if tmp:
		#print('12312313121mvjshdfu')
		port=re.findall("[0-9]+",tmp)[0]
		print(port)
		os.system("kill "+str(port))
		print('Last one killed succeed')

	print("Starting Server")
	os.system("cd '/Users/yuanyige/Library/Mobile Documents/com~apple~CloudDocs/Work/syn/fileSYNserver';python3 server.py" )

	print("Hello Father")



