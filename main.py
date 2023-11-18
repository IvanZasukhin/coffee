import sqlite3
import sys

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MyProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # from ui file
        # self.setupUi(self) # from py file (need to import class from generated .py file)
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.click_pushButton)

    def click_pushButton(self):
        data = self.cur.execute("Select * from id_coffee", ).fetchall()
        try:
            self.tableWidget.setColumnCount(len(data[0]))
            self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", 'молотый/в зернах',
                                                        'описание вкуса', 'цена', 'объем упаковки'])
        except IndexError:
            self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(el)))

    def closeEvent(self, even):
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyProgram()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
