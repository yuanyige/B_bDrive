'''
ItemClasses
'''
from PyQt5.QtCore import Qt,QRectF
from PyQt5.QtGui import QIcon,QPainter,QBrush,QColor,QLinearGradient
from PyQt5.QtWidgets import *

class QTextInput(QLineEdit):
	def __init__(self, *args):
		super(QTextInput, self).__init__(*args)

class QButton(QPushButton):
	def __init__(self, *args):
		super(QButton, self).__init__(*args)

class QFileButton(QPushButton):
	def __init__(self, *args):
		super(QFileButton, self).__init__(*args)

class Toast(QMessageBox):
	def __init__(self, *args):
		super(Toast, self).__init__(*args)

class QTextLabel(QLabel):
	def __init__(self, *args):
		super(QTextLabel, self).__init__(*args)

class QMenuButton(QPushButton):
	def __init__(self, *args):
		super(QMenuButton, self).__init__(*args)

class QBorderWidget(QWidget):
	def __init__(self,*args):
		super(QBorderWidget, self).__init__(*args)
		self.color=QColor(0,0,0,0)

	def paintEvent(self, ev):
		painter = QPainter(self)
		painter.setPen(QColor(0,0,0,255));
		painter.setRenderHint(QPainter.Antialiasing)
		gradient = QLinearGradient(QRectF(self.rect()).topLeft(),QRectF(self.rect()).bottomLeft())
		painter.setBrush(QBrush(self.color));
		painter.drawRoundedRect(self.rect(),0,0)
		painter.end()
