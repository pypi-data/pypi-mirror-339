import shutil
import sys
import re
from PyQt6.QtGui import QColor
from screeninfo import get_monitors
import pathlib
import os
import math
import platform
import subprocess

from PyQt6 import QtGui
from PyQt6.QtWidgets import (
	QApplication, 
	QWidget, 
	QMainWindow, 
	QGroupBox, 
	QVBoxLayout, 
	QHBoxLayout, 
	QListWidget,
	QPushButton, 
	QButtonGroup, 
	QRadioButton,
	QSystemTrayIcon,
	QMenu,
	QFileDialog,
	QTableWidget,
	QTableWidgetItem,
	QAbstractItemView,
	QLineEdit,
	QInputDialog,
)
from PyQt6.QtCore import Qt

from general import Casting, Mongo, Mainroad
from singletons import Students

def get_student_dir(student):
	students_o = Students()
	stdur = Mainroad.get_student_dirs_path()
	return students_o.make_student_folder_path_from_d(student)

class AirfieldWindow(QMainWindow):
	_windowsize = (900, 700)
	_gutter = 20
	_canvas = None
	_students = None
	_studentdicts = dict()
	_downloaddir = ""
	_m = None
	_groups = None
	_spekenbonen = False
	_assignment = None
	
	def __init__(self):
		super().__init__()
		self.initializeUI()

	def __del__(self):
		try:
			del self._m
		except:
			pass
	def initializeUI(self):
		self._downloaddir = str(pathlib.Path.home() / "Downloads")
		self._m = Mongo(collection='sys')

		# scherm afmetingen
		for m in get_monitors():
			height = m.height
			width = m.width
			break		
		# center point on screen
		center_x = int(width/2 - self._windowsize[0] / 2)
		center_y = 100 # (height/2 - self._windowsize[1] / 2)		
		self.setGeometry(center_x, center_y, self._windowsize[0], self._windowsize[1])
		self.setWindowTitle('Move BB uploads to Student dirs')

		# place in mainwindow
		widget = QWidget()
		columns = QHBoxLayout()
		columns.setSpacing(0) # between widgets
		columns.setContentsMargins(0, 0, 0, 0) # around boxlayout

		# create label with canvas
		columns.addWidget(self.create_students_table())		
		# add table with students
		columns.addWidget(self.create_files_listbox())
		# opvullen 
		# columns.addStretch()
		
		# stick it all together
		widget.setLayout(columns)
		self.setCentralWidget(widget)
		self.show()	
		
	def create_students_table(self):
		# two radio buttons for courses
		# make list with students
		layout = QVBoxLayout()
		layout.setSpacing(self._gutter) # between widgets
		layout.setContentsMargins(self._gutter*2, self._gutter*2, self._gutter, self._gutter*2) # around boxlayout		

		# buttons die je eenmaal gebruikt
		cwf = QWidget()
		cwf.setStyleSheet('border: 2px solid dimgray; max-width: 400px;')
		buttonslayout = QHBoxLayout()
		cwf.setLayout(buttonslayout)

		btn_dir = QPushButton("Choose Dir")
		btn_dir.setStyleSheet("background-color: white; color: black;")
		btn_dir.clicked.connect(self.dir_clicked)
		buttonslayout.addWidget(btn_dir)

		# naam van de summative
		self._assignment = QLineEdit()
		self._assignment.setStyleSheet("background-color: white; color: black;")
		self._assignment.setEnabled(False)
		buttonslayout.addWidget(self._assignment)

		# radiobuttons courses
		cw = QWidget()
		cw.setStyleSheet('border: 2px solid dimgray;')

		# get stuff from database
		self._m.set_collection('sys')
		courses = self._m.read(where={'sysl': 's_course', 'status': 1})
		self._groups = self._m.read(where={'sysl': 's_group', 'status': 1})

		self._radio_courses = QButtonGroup()
		self._radio_courses.buttonClicked.connect(self.course_changed)
		courseskader = QGroupBox("Courses")
		courseslayout = QHBoxLayout()
		cw.setLayout(courseslayout)
		for course in courses:
			c = QRadioButton(f"{course['name']}")
			self._radio_courses.addButton(c, int(course['id']))
			courseslayout.addWidget(c)
		courseslayout.addStretch()
		
		self._students = QTableWidget(0, 3)
		self._students.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
		self._students.hasAutoScroll()
		self._students.verticalScrollBar().setStyleSheet('width: 20px;')
		self._students.verticalHeader().setVisible(False)
		self._students.horizontalHeader().setVisible(False)

		self._students.horizontalHeader().stretchLastSection()
		self._students.horizontalHeader().resizeSection(0, 50)
		self._students.horizontalHeader().resizeSection(1, 100)
		self._students.horizontalHeader().setStretchLastSection(True)
		self._students.setStyleSheet('width: 100%;  border: 2px solid dimgray; background-color: #333; padding: 10px;')
		self._students.clicked.connect(self.student_clicked)

		# layout.addLayout(courseslayout)
		layout.addWidget(cwf)
		layout.addWidget(cw)
		layout.addWidget(self._students)
		
		lawi = QWidget()
		lawi.setStyleSheet('border-radius: 10px;')
		lawi.setLayout(layout)		
		return lawi			

	def create_files_listbox(self):
		layout = QVBoxLayout()
		layout.setSpacing(self._gutter) # between widgets
		layout.setContentsMargins(self._gutter, self._gutter*2, self._gutter*2, self._gutter*2) # around boxlayout
		
		# buttons widget met layout
		cwf = QWidget()
		cwf.setStyleSheet('border: 2px solid dimgray; max-width: 400px;')
		buttonslayout = QHBoxLayout()
		cwf.setLayout(buttonslayout)

		btn_auto = QPushButton("Auto")
		btn_auto.setStyleSheet("background-color: darkorange;")
		btn_auto.clicked.connect(self.auto_clicked)
		buttonslayout.addWidget(btn_auto)

		# move button
		btn_move = QPushButton("Move")
		btn_move.setStyleSheet("background-color: dodgerblue;")
		btn_move.clicked.connect(self.move_clicked)
		buttonslayout.addWidget(btn_move)

		# file browser
		self._files = QListWidget()
		# self._files.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		self._files.setStyleSheet('border: 2px solid dimgray; max-width: 400px; padding: 5px; background-color: #333; color: white;')
		self._files.clicked.connect(self.file_clicked)
		
		layout.addWidget(cwf)
		layout.addWidget(self._files)
		
		lawi = QWidget()
		lawi.setStyleSheet('border-radius: 10px;')
		lawi.setLayout(layout)		
		return lawi		
	
	def student_clicked(self):
		rij = self._students.currentRow()
		kolom = self._students.currentColumn()
		if kolom == 0:
			id = int(self._students.currentItem().text())
			student = self._studentdicts[id]
			student_dir = get_student_dir(student)
			try:
				if platform.system() == "Windows":
					os.startfile(student_dir)
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", student_dir])
				else:
					subprocess.Popen(["xdg-open", student_dir])
			except Exception as e:
				pass
		self._students.selectRow(rij)

	def file_clicked(self, event):
		item = self._files.currentItem()	
		print(f"file: {item.text()}")

	def get_group(self, groupid: int):
		for g in self._groups:
			if g['id'] == groupid:
				return g
		return None

	def course_changed(self):
		self._students.clear()
		course_id = self._radio_courses.checkedId()

		studenten = list()
		self._m.set_collection('students')
		studenten = self._m.read(where={'s_course': course_id, 's_status': {'$in': [20, 21, 22, 23]}})
		studenten = sorted(studenten, key=lambda d: d['firstname'])
		self._studentdicts = dict()

		self._students.setRowCount(len(studenten))
		for i in range(len(studenten)):
			student = studenten[i]
			self._studentdicts[student['id']] = student
			groep = self.get_group(student['s_group'])

			qtwi = QTableWidgetItem(str(student['id']))
			qtwi.setBackground(self.qcolor_from_css(groep['color']))
			qtwi.setForeground(self.contrast_from_css(groep['color']))
			self._students.setItem(i, 0, qtwi)

			qtwi = QTableWidgetItem(groep['name'])
			qtwi.setForeground(QtGui.QColor("white"))
			self._students.setItem(i, 1, qtwi)

			qtwi = QTableWidgetItem(f"{student['firstname']} {student['lastname']}")
			qtwi.setForeground(QtGui.QColor("white"))
			self._students.setItem(i, 2, qtwi)

	def refresh_dir_view(self):
		files = list()
		for f in os.listdir(self._downloaddir):
			if f.startswith('.'):
				continue
			if f.endswith('.ini'):
				continue
			if not os.path.isfile(os.path.join(self._downloaddir, f)):
				continue
			files.append(f)
		files.sort()

		self._files.clear()
		for f in files:
			self._files.addItem(f)

	def dir_clicked(self):
		# filedialog open dir
		qfd = QFileDialog.getExistingDirectory(caption="Kies Download Dir", directory=self._downloaddir)
		if not qfd:
			return
		antwoord, ok = QInputDialog.getText(self, 'Name of the assignment', '')
		if not antwoord:
			return
		if antwoord.strip() == "":
			return
		antwoord = antwoord.replace(' ', '_')
		self._assignment.setText(antwoord)
		# contents in listbox self._files
		self._downloaddir = qfd
		self.refresh_dir_view()

	def auto_move_single_student(self, student) -> bool:
		student_dir = get_student_dir(student)
		ass = self._assignment.text()
		if not os.path.isdir(os.path.join(student_dir, 'summative', ass)):
			os.mkdir(os.path.join(student_dir, 'summative', ass))

		bbname = student['bb_name']
		# get all files from student
		all_items = list()
		for i in range(0, self._files.count()):
			self._files.setCurrentRow(i)
			f = self._files.currentItem().text()
			if not f.startswith(bbname):
				continue
			all_items.append(f)

		if len(all_items) == 0:
			return False

		# move all files
		snrs = ["", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_"]
		for item in all_items:
			# for not overwriting stuff
			nr = 0
			item_up = item
			while os.path.exists(os.path.join(student_dir, 'summative', ass, item_up)):
				nr += 1
				item_up = item.replace('] ', f"] {str(nr)*nr}_")
			if not self._spekenbonen:
				shutil.move(os.path.join(self._downloaddir, item), os.path.join(student_dir, 'summative', ass, item_up))
		return True

	def auto_clicked(self):
		print("auto geklikt")
		if self._students.rowCount() == 0:
			print("geen studenten")
			return
		if self._files.count() == 0:
			print("geen files")
			return

		self._m.set_collection('students')
		# start at no 0 in students list
		# select student
		for i in range(0, self._students.rowCount()):
			self._students.selectRow(i)
			self._students.setCurrentCell(i, 0)
			try:
				id = int(self._students.currentItem().text())
				student = self._studentdicts[id]
				# if not student field bb_name has contents, continue
				bbname = student['bb_name']
			except Exception as e:
				continue

			if self.auto_move_single_student(student):
				# geef student kleur
				self._students.item(i, 1).setBackground(QtGui.QColor("orange"))
				self._students.item(i, 2).setBackground(QtGui.QColor("orange"))

			# refresh list view
			self.refresh_dir_view()
		
	def move_clicked(self):
		pattern =  re.compile(r"\[.*\]")

		print("# get student from student table view")
		try:
			row = self._students.currentRow()
			self._students.setCurrentCell(row, 0)
			id = int(self._students.currentItem().text())
			student = self._studentdicts[id]
			student_dir = get_student_dir(student)
		except Exception as e:
			print("geen student", e)
			return
		ass = self._assignment.text()
		print('ass', ass)
		if not os.path.isdir(os.path.join(student_dir, 'summative', ass)):
			os.mkdir(os.path.join(student_dir, 'summative', ass))

		# get selected student name from listview
		try:
			item = self._files.currentItem().text()
			item_name = re.findall(pattern, item)[0]
		except:
			return

		# get all files from student
		all_items = list()
		for f in os.listdir(self._downloaddir):
			if not f.startswith(item_name):
				continue
			all_items.append(f)

		# move all files
		snrs = ["", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_"]
		for item in all_items:
			# for not overwriting stuff
			nr = 0
			item_up = item
			while os.path.exists(os.path.join(student_dir, 'summative', item_up)):
				nr += 1
				item_up = item.replace('] ', f"] {str(nr)*nr}_")
			shutil.move(os.path.join(self._downloaddir, item), os.path.join(student_dir, 'summative', ass, item_up))

		# refresh list view
		self.refresh_dir_view()

		# add name to student in mongo
		self._m.set_collection('students')
		if not self._spekenbonen:
			self._m.update_one(where={'id': id}, what={'$set': {'bb_name': item_name}}, upsert=False)
		
	def qcolor_from_css(self, color: str):
		qc = QtGui.QColor()
		if color.startswith('#'):
			# hex
			return qc.fromString(color)
		elif color.startswith('rgba('):
			# rgba
			color = color.replace('rgba(', '').replace(')', '')
			color = color.split(',')
			try:
				qc.setRed(int(color[0].strip()))
				qc.setGreen(int(color[1].strip()))
				qc.setBlue(int(color[2].strip()))
				alfa = int(float((color[3].strip()))*100)
				qc.setAlpha(alfa)
			except Exception as e:
				print(e)
				
				return qc.fromString("yellow")
			return qc
			
		elif color.startswith('rgb('):
			# rgba
			color = color.replace('rgb(', '').replace(')', '')
			color = color.split(',')
			try:
				qc.setRed(int(color[0]))
				qc.setGreen(int(color[1]))
				qc.setBlue(int(color[2]))
			except:
				return qc.fromString("yellow")
			return qc			
		else:
			# colorname
			return qc.fromString(color)

	def contrast_from_css(self, color: str):
		qc = self.qcolor_from_css(color)
		total = qc.red() + qc.green() + qc.blue()
		hsp = math.sqrt(
			0.299 * (qc.red() *  qc.red()) +
			0.587 * (qc.green() * qc.green()) +
			0.114 * (qc.blue() * qc.blue())
		)
		if hsp > 127.5:
			return QColor.fromString("black")
		else:
			return QColor.fromString("white")
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	pad = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(pad, "static/dnd.css"), "r") as f:
		_style = f.read()
		app.setStyleSheet(_style)
		
	# icon = QtGui.QIcon("assets/head.png")
	window = AirfieldWindow()
	app.exec()
	sys.exit()	