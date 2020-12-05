from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sqlite3
from filtering import Ui_MainWindow


class DataBase(QMainWindow, Ui_MainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.show()
        self.con = sqlite3.connect("scrabble.db")
        self.setStyleSheet('.QWidget {background-image: url(background_2.jpg);}')
        self.filter0.clicked.connect(self.filter)
        self.filter1.clicked.connect(self.filter)
        self.btn_back.clicked.connect(self.back)
        self.queue = 0
        cur = self.con.cursor()
        self.comboBox.addItems(['все', *[item[0] for item in cur.execute("SELECT name FROM participants").fetchall()]])
        result = cur.execute("""SELECT * FROM participants""").fetchall()
        self.fill_table(result)
        self.btn_search.clicked.connect(self.search)

    def search(self):
        cur = self.con.cursor()
        if self.comboBox.currentText() == "по id":
            result = cur.execute("""SELECT * FROM all_games_played ORDER BY id DESC""").fetchall()
        elif self.comboBox.currentText() == "по баллам":
            result = cur.execute("""SELECT * FROM all_games_played ORDER BY points DESC""").fetchall()
        elif self.comboBox.currentText() != "все":
            result = cur.execute("""SELECT * FROM participants WHERE name = ?""",
                                 (self.comboBox.currentText(),)).fetchall()
        else:
            result = cur.execute("""SELECT * FROM participants""").fetchall()
        self.fill_table(result)

    def filter(self):
        if self.sender().styleSheet() != 'QPushButton {background-color:"white"}':
            self.sender().setStyleSheet('QPushButton {background-color:"white"}')
            eval(f'self.filter{self.queue}.setStyleSheet("QPushButton {{background-color:None}}")')
        cur = self.con.cursor()
        self.comboBox.clear()
        if self.sender().text() == "по участникам":
            self.queue = 0
            self.comboBox.addItems(['все', *[item[0] for item in cur.execute("SELECT name FROM participants").fetchall()]])
            result = cur.execute("""SELECT * FROM participants""").fetchall()
        else:
            result = cur.execute('SELECT * FROM all_games_played ORDER BY id DESC').fetchall()
            self.queue = 1
            self.comboBox.addItems(['по id', 'по баллам'])
        self.fill_table(result)

    def back(self):
        self.main_window.show()
        self.hide()

    def fill_table(self, result):
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.main_window.unexpected_interrupts = 1
        self.main_window.game_over()
        self.con.close()
