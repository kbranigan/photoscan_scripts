#creates masks for cameras in the active chunk, based on user defined color and tolerance

#compatibility PhotoScan Pro 1.1.0

import PhotoScan
from PySide import QtGui, QtCore

class MaskByColor(QtGui.QDialog):

	def __init__(self, parent):
	
		QtGui.QDialog.__init__(self, parent)
		
		self.color = QtGui.QColor(0, 0, 0)
		red, green, blue = self.color.red(), self.color.green(), self.color.blue()

		self.setWindowTitle("Masking by color:")
		
		self.btnQuit = QtGui.QPushButton("Quit")
		self.btnQuit.setFixedSize(100,50)
		
		self.btnP1 = QtGui.QPushButton("Mask")
		self.btnP1.setFixedSize(100,50)
		
		self.pBar = QtGui.QProgressBar()
		self.pBar.setTextVisible(False)
		self.pBar.setFixedSize(130, 50)
		
		self.selTxt = QtGui.QLabel()
		self.selTxt.setText("Apply to:")
		self.selTxt.setFixedSize(100, 25)	
		
		self.radioBtn_all = QtGui.QRadioButton("all cameras")
		self.radioBtn_sel = QtGui.QRadioButton("selected cameras")
		self.radioBtn_all.setChecked(True)
		self.radioBtn_sel.setChecked(False)
		
		self.colTxt = QtGui.QLabel()
		self.colTxt.setText("Select color:")
		self.colTxt.setFixedSize(100, 25)	
		
		strColor = "{:0>2d}{:0>2d}{:0>2d}".format(int(hex(red)[2:]), int(hex(green)[2:]), int(hex(blue)[2:])) 
		self.btnCol = QtGui.QPushButton(strColor)
		self.btnCol.setFixedSize(80, 25)	
		pix = QtGui.QPixmap(10, 10)
		pix.fill(self.color)
		icon = QtGui.QIcon()
		icon.addPixmap(pix)
		self.btnCol.setIcon(icon)
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Button, self.color)
		self.btnCol.setPalette(palette)
		self.btnCol.setAutoFillBackground(True)
		
		self.txtTol = QtGui.QLabel()
		self.txtTol.setText("Tolerance:")
		self.txtTol.setFixedSize(100, 25)	
		
		self.sldTol = QtGui.QSlider()
		self.sldTol.setOrientation(QtCore.Qt.Orientation.Horizontal)
		self.sldTol.setMinimum(0)
		self.sldTol.setMaximum(99)
		
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.pBar)
		hbox.addWidget(self.btnP1)
		hbox.addWidget(self.btnQuit)		
		
		layout = QtGui.QGridLayout()   
		layout.setSpacing(5)
		layout.addWidget(self.selTxt, 0, 0)
		layout.addWidget(self.radioBtn_all, 1, 0)
		layout.addWidget(self.radioBtn_sel, 2, 0)
		layout.addWidget(self.colTxt, 0, 1)
		layout.addWidget(self.btnCol, 1, 1)
		layout.addWidget(self.txtTol, 0, 2)
		layout.addWidget(self.sldTol, 1, 2)
		layout.addLayout(hbox, 3, 0, 5, 3)
		self.setLayout(layout)  		
		
		proc_mask = lambda : self.maskColor()
		proc_color = lambda : self.changeColor()
		
		QtCore.QObject.connect(self.btnP1, QtCore.SIGNAL("clicked()"), proc_mask)
		QtCore.QObject.connect(self.btnCol, QtCore.SIGNAL("clicked()"), proc_color)
		QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))	

		self.exec()
		
	def changeColor (self):
	
		color = QtGui.QColorDialog.getColor()
	
		self.color = color
		red, green, blue = color.red(), color.green(), color.blue()	
		if red < 16:
			red = "0" + hex(red)[2:]
		else:
			red = hex(red)[2:]
		if green < 16:
			green = "0" + hex(green)[2:]
		else:
			green = hex(green)[2:]
		if blue < 16:
			blue = "0" + hex(blue)[2:]
		else:
			blue = hex(blue)[2:]
		
		strColor = red + green + blue
		self.btnCol.setText(strColor)
		
		pix = QtGui.QPixmap(10, 10)
		pix.fill(self.color)
		icon = QtGui.QIcon()
		icon.addPixmap(pix)
		self.btnCol.setIcon(icon)
		
		palette = self.btnCol.palette()
		palette.setColor(QtGui.QPalette.Button, self.color)
		self.btnCol.setPalette(palette)
		self.btnCol.setAutoFillBackground(True)
		
		return True

	def maskColor (self):
	
		tolerance = 10
		tolerance = self.sldTol.value()
		
		self.sldTol.setDisabled(True)
		self.btnCol.setDisabled(True)
		self.btnP1.setDisabled(True)
		self.btnQuit.setDisabled(True)
	
		chunk = PhotoScan.app.document.chunk
		mask_list = list()
		if self.radioBtn_sel.isChecked():
			for photo in chunk.cameras:
				if photo.selected:
					mask_list.append(photo)
		elif self.radioBtn_all.isChecked():
			mask_list = list(chunk.cameras)
			
		if not len(mask_list):
			PhotoScan.app.messageBox("Nothing to mask!")
			return False

		color = self.color
		red, green, blue = color.red(), color.green(), color.blue()

		processed = 0
		
		for camera in mask_list:
			for frame in camera.frames:
				QtGui.qApp.processEvents()
				mask = PhotoScan.utils.createDifferenceMask(frame.photo.image(), (red, green, blue), tolerance, False)
				m = PhotoScan.Mask()
				m.setImage(mask)
				frame.mask = m
				processed += 1
				self.pBar.setValue(int(processed / len(mask_list) / len(chunk.frames) * 100))
				
			
		print("Masking finished. " + str(processed) + " images masked.\n")
		
		self.sldTol.setDisabled(False)
		self.btnCol.setDisabled(False)
		self.btnP1.setDisabled(False)
		self.btnQuit.setDisabled(False)
		
		return True		
		
def main():

	global doc
	doc = PhotoScan.app.document

	app = QtGui.QApplication.instance()
	parent = app.activeWindow()
	
	dlg = MaskByColor(parent)
		
		
PhotoScan.app.addMenuItem("Custom/Masking by color", main)