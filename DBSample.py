from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3
from main import main_window


class DataBase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        uic.loadUi('filtering.ui', self)
        self.con = sqlite3.connect("scrabble.db")
        self.setStyleSheet('.QWidget {background-image: url(background_2.jpg);}')
        cur = self.con.cursor()
        self.comboBox.addItems([item[0] for item in cur.execute("SELECT name FROM participants").fetchall()])
        result = cur.execute("""SELECT * FROM participants""").fetchall()
        self.fill_table(result)
        self.pushButton.clicked.connect(self.filtering_by_players)
        self.pushButton_2.clicked.connect(self.filtering_by_winners)
        self.btn_back.clicked.connect(self.back)

    def back(self):
        # .show()
        self.hide()

    def fill_table(self, result):
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def filtering_by_players(self):
        cur = self.con.cursor()
        if self.comboBox.currentText() != "все":
            result = cur.execute("""SELECT * FROM participants WHERE name = ?""",
                                 (self.comboBox.currentText(),)).fetchall()
        else:
            result = cur.execute("""SELECT * FROM participants""").fetchall()
        self.fill_table(result)

    def filtering_by_winners(self):
        cur = self.con.cursor()
        result = cur.execute('SELECT * FROM all_games_played').fetchall()
        if self.comboBox_2.currentText() == "по id":
            result = cur.execute("""SELECT * FROM all_games_played ORDER BY id""").fetchall()
        elif self.comboBox_2.currentText() == "по баллам":
            result = cur.execute("""SELECT * FROM all_games_played ORDER BY points""").fetchall()
        self.fill_table(result)

    def closeEvent(self, event):
        main_window.unexpected_interrupts = 1
        main_window.game_over()
        self.con.close()


db = DataBase()
