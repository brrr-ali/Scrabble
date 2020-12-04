import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import pymorphy2
import random
from PyQt5 import uic
import sqlite3
from DBSample import db

SIZE_FIELD = 15


class Button(QPushButton):
    # создаем класс Button наследуемый от QPushButton, но обьекты этого класса можно передвигать
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        # передаем координаты кнопки, которую начали передвигать в функцию run в классе Example
        main_window.run(e.globalX() - main_window.x())
        QPushButton.mouseMoveEvent(self, e)
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)


class MainWindow(QMainWindow, ):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн

        self.initUI()

    def initUI(self):
        self.statistics.clicked.connect(self.statistic)
        self.count_letters_and_price = {'А': [10, 1], 'Б': [3, 3], 'В': [5, 2], 'Г': [3, 3],
                                        'Д': [5, 2], 'Е': [9, 1], 'Ж': [2, 5], 'З': [2, 5],
                                        'И': [8, 1], 'Й': [4, 2], 'К': [6, 2], 'Л': [4, 2],
                                        'М': [5, 2], 'Н': [8, 1], 'О': [10, 1], 'П': [6, 2],
                                        'Р': [6, 2], 'С': [6, 2], 'Т': [5, 2], 'У': [3, 3],
                                        'Ф': [1, 10], 'Х': [2, 5], 'Ц': [1, 10], 'Ч': [2, 5],
                                        'Ш': [1, 10], 'Щ': [1, 10], 'Ъ': [1, 10], 'Ы': [2, 5],
                                        'Ь': [2, 5], 'Э': [1, 10], 'Ю': [1, 10],
                                        'Я': [3, 3]}  # Строение словаря: 'буква': [количество буквы, цена]
        # self.count_player = 0
        self.setGeometry(200, 30, 800, 600)
        self.btn_check.clicked.connect(self.check)
        self.opening_words_focused = False
        self.btn_replaced_letters.clicked.connect(self.changing_letters)
        self.setAcceptDrops(True)
        self.field, s, s2, self.coords, self.new_word = [], [], [], [], []
        self.queue = 0
        self.skipping_move = 0
        self.unexpected_interrupts = 0
        for i in range(4):
            eval(f'self.player{i + 1}.hide()')
        x, y = 10, 10
        # создаем поле
        for j in range(SIZE_FIELD):
            s, s2 = [], []
            for i in range(SIZE_FIELD):
                self.name = QPushButton(self)
                self.name.move(x, y)
                self.name.resize(35, 35)
                x += 35
                # раскрашиваем поле
                if i == j or i + j == SIZE_FIELD - 1:
                    if i == 0 or i == SIZE_FIELD - 1:
                        self.name.setStyleSheet('QPushButton {background-color: #c4544d}')
                    elif 1 <= i <= 4 or 10 <= i <= 13:
                        self.name.setStyleSheet('QPushButton {background-color: #4d4dc4}')
                    elif i == 6 or i == 8:
                        self.name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i + j == 10 or i - j == 4:
                    if j == 1 or j == 9:
                        self.name.setStyleSheet('QPushButton {background-color: #cfca42}')
                    elif j == 2 or j == 3 or j == 7 or j == 8:
                        self.name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i + j == 18 or j - i == 4:
                    if j == 5 or j == 13:
                        self.name.setStyleSheet('QPushButton {background-color: #cfca42}')
                    elif j == 6 or j == 7 or j == 11 or j == 12:
                        self.name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i == 0 or i == SIZE_FIELD - 1:
                    if j == 3 or j == 11:
                        self.name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                    elif j == 7:
                        self.name.setStyleSheet('QPushButton {background-color: #c4544d}')
                elif j == 0 or j == SIZE_FIELD - 1:
                    if i == 3 or i == 11:
                        self.name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                    elif i == 7:
                        self.name.setStyleSheet('QPushButton {background-color: #c4544d}')
                s.append(self.name)
                s2.append([self.name.x(), self.name.y()])
            self.field.append(s)
            self.coords.append(s2)
            y += 35
            x = 10
        for i in range(2, 4):
            eval(f'self.name{i + 1}.hide()')
        self.btn_choice = []
        self.players = []
        self.alphabet = list(self.count_letters_and_price.keys())
        self.delete_used_letters()
        self.btn_remember.clicked.connect(self.remember)
        for i in range(2, 4):
            eval(f'self.checkBox_{i + 1}.stateChanged.connect(self.player_added)')
        self.count_player = 2
        x = 10
        # создаем передвижимые кнопки
        for i in range(7):
            name = f"btn{i}"
            self.name = Button('', self)
            self.name.move(x, 540)
            self.name.resize(35, 35)
            self.name.hide()
            self.btn_choice.append(self.name)
            x += 35

    def delete_used_letters(self):
        i = 0
        while i < len(self.alphabet):
            if self.count_letters_and_price[self.alphabet[i]][0] <= 0:
                # удаляем буквы, которые кончились
                if 0 <= self.alphabet.index(self.alphabet[i]) < len(self.alphabet):
                    del self.alphabet[self.alphabet.index(self.alphabet[i])]
            i += 1

    def player_added(self):
        self.count_player = 0
        for i in range(4):
            if eval(f'self.checkBox_{i + 1}.isChecked()'):
                eval(f'self.name{i + 1}.show()')
                self.count_player += 1
            else:
                eval(f'self.name{i + 1}.hide()')

    def run(self, coord_x_btn_alphabet):
        i_btn_choice = 0
        # проходим по всем буквам и пытаемся узнать какую перетащили
        for i in range(7):
            if self.btn_choice[i].x() <= coord_x_btn_alphabet <= self.btn_choice[i].x() + self.btn_choice[i].width():
                i_btn_choice = i
                break
        self.i_btn_choice = i_btn_choice

    def remember(self):
        for el in self.btn_choice:
            el.show()
        self.players = []

        self.btn_check.setEnabled(True)
        # self.btn_replaced_letters.setEnabled(True)
        self.replaced_letters.setEnabled(True)
        for i in range(self.count_player):
            eval(f"self.player{i + 1}").setText(eval(f"self.name{i + 1}.text()") + '\n 0 баллов')
            s = []
            self.delete_used_letters()
            for j in range(7):
                n = random.choice(self.alphabet)
                self.count_letters_and_price[n][0] -= 1
                s.append(n)
            self.players.append([eval(f'self.player{i + 1}'), 0, s])
        i = 0
        # заполняем кнопки буквами игрока, который будет первым ходить
        for el in self.btn_choice:
            el.setText(self.players[self.queue][2][i] + '\n' + str(
                self.count_letters_and_price[self.players[self.queue][2][i]][1]))
            i += 1
        self.all_letters_to_replace = []
        self.number_of_remaining_letters.setText('Осталось букв: ' + str(self.print_number_of_remaining_letters()))
        self.delete_used_letters()
        self.skipping_move = 0
        self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #c6c6ec}')
        for i in range(4):
            eval(f'self.name{i + 1}.hide()')
            eval(f'self.checkBox_{i + 1}.hide()')
        self.label.setText('')

        self.btn_remember.hide()
        for i in range(self.count_player):
            eval(f'self.player{i + 1}.show()')

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        x1, y1 = 0, 0
        if self.replaced_letters.y() <= position.y() <= self.replaced_letters.y() + \
                self.replaced_letters.height() and \
                self.replaced_letters.x() <= position.x() <= \
                self.replaced_letters.x() + self.replaced_letters.width():
            self.btn_choice[self.i_btn_choice].setEnabled(False)
            self.all_letters_to_replace.append(self.i_btn_choice)
            self.btn_check.setEnabled(False)
        else:
            self.skipping_move = 0
            for i in range(SIZE_FIELD):
                if self.coords[0][i][0] <= position.x() <= self.coords[0][i][0] + 50:
                    x1 = i
                if self.coords[i][0][1] <= position.y() <= self.coords[i][0][1] + 50:
                    y1 = i
            if self.field[y1][x1].text() == '':
                self.new_word.append((x1, y1, self.players[self.queue][2][self.i_btn_choice], self.i_btn_choice))
                self.field[y1][x1].setText(self.players[self.queue][2][self.i_btn_choice])
                self.btn_choice[self.i_btn_choice].setEnabled(False)
            e.setDropAction(Qt.MoveAction)
            e.accept()

    def print_number_of_remaining_letters(self):
        count = 0
        for value in self.count_letters_and_price.values():
            count += value[0]
        return count

    def game_over(self):
        if self.print_number_of_remaining_letters() == 0 or \
                self.skipping_move == self.count_player * 2 or self.unexpected_interrupts:
            for el in self.players:
                self.add_or_change_db(el[0].text().split('\n')[0], el[1])
            maxim = 0
            maxim_name = []
            self.players.sort(key=lambda x: x[1], reverse=True)
            for el in self.players:
                if el[1] >= maxim:
                    maxim = el[1]
                    maxim_name.append([el[0].text().split('\n')[0], el[1]])
            if len(maxim_name) == self.count_player:
                self.error.setText('Игра окончена! Ничья!')
            else:
                self.error.setText('Игра окончена! Наибольшее количество баллов набрали: '
                                   + ', '.join(el[0] for el in maxim_name))
            self.add_winner_in_bd(maxim_name)
            return True
        return False

    def add_winner_in_bd(self, names_and_points):
        con = sqlite3.connect("scrabble.db")
        cur = con.cursor()
        if names_and_points:
            cur.execute(
                f"INSERT INTO all_games_played(name_winner, points) VALUES "
                f"{' '.join(str(el[0]) for el in names_and_points) + '', '' + str(names_and_points[0][1])}")
            con.commit()
        con.close()

    def add_or_change_db(self, name, point):
        con = sqlite3.connect("scrabble.db")
        cur = con.cursor()
        execute = cur.execute("select points from participants where name = ?", (name,)).fetchone()
        if execute:
            cur.execute("""UPDATE participants set points = ? WHERE name = ?""",
                        (str(execute[0]) + ' ' + str(point), name))
        else:
            cur.execute("INSERT INTO participants (name, points) values (?, ?)", (name, point))
            db.comboBox.addItem(name)
        con.commit()
        con.close()

    def check(self):
        word_analysis = 0
        if len(self.new_word) > 0:
            self.new_word_all_letters = self.new_word
            self.new_word.sort(key=lambda x: (x[0], x[1]))
            new_word2 = []
            error = 0
            flag1, flag2 = 0, 0
            for el in self.new_word:
                if el[0] != self.new_word[0][0]:
                    flag1 = 1
                if el[1] != self.new_word[0][1]:
                    flag2 = 1
            if flag1 and flag2:
                error = 1
            if error == 0:
                new_word = ''
                if self.opening_words_focused is False:
                    for el in self.new_word:
                        new_word += el[2]
                else:
                    if self.new_word[0][0] == self.new_word[-1][0]:
                        x, y_lower, y_upper = self.new_word[0][0], self.new_word[-1][1], self.new_word[0][1]
                        while self.field[y_lower][x].text() != '' and y_lower < SIZE_FIELD:
                            y_lower += 1
                        while self.field[y_upper][x].text() != '' and y_upper >= 0:
                            y_upper -= 1
                        if y_lower - y_upper - 1 == len(self.new_word):
                            error = 1
                        else:
                            for i in range(y_upper + 1, y_lower):
                                new_word2.append((self.new_word[1][0], i, self.field[i][x].text(), 0))
                                new_word += self.field[i][x].text()
                    elif self.new_word[0][1] == self.new_word[-1][1]:
                        y, x_lower, x_upper = self.new_word[0][1], self.new_word[-1][0], self.new_word[0][0]
                        while self.field[y][x_lower].text() != '' and x_lower < SIZE_FIELD:
                            x_lower += 1
                        while self.field[y][x_upper].text() != '' and x_upper >= 0:
                            x_upper -= 1
                        if x_lower - x_upper - 1 == len(self.new_word):
                            error = 1
                        else:
                            new_word2 = []
                            for i in range(x_upper - 1, x_lower):
                                new_word2.append(
                                    (i, self.new_word[0][1], self.field[self.new_word[0][1]][i].text(), 0))
                                new_word += self.field[self.new_word[0][1]][i].text()
                    if new_word2:
                        self.new_word_all_letters = new_word2
                analysis = pymorphy2.MorphAnalyzer().parse(new_word)
                for el in analysis:
                    if el.tag.POS == 'NOUN' and 'nomn' in el.tag and \
                            (el.tag.number == 'sing') and 'Name' not in el.tag:
                        word_analysis = 1
                        break
            if word_analysis:
                self.scoring_points()
            elif word_analysis == 0 or error:
                for el in self.btn_choice:
                    if el.isEnabled() is False:
                        el.setEnabled(True)
                for el in self.new_word:
                    if el[2] in self.count_letters_and_price.keys():
                        self.count_letters_and_price[el[2]][0] += 1
                        self.field[el[1]][el[0]].setText('')
                self.error.setText('Не удовлетворяет требованиям к новым словам, попробуйте снова')
            self.new_word_all_letters.clear()
            self.new_word.clear()

    def scoring_points(self):
        summa, all_summa = 0, 0
        additional_point = ''
        additional_multiplication = ''
        for el in self.new_word_all_letters:
            if el[2]:
                summa += self.count_letters_and_price[el[2]][1]
                colour = self.field[el[1]][el[0]].styleSheet()[31:-1]
                if colour == '#c4544d':
                    additional_multiplication += '*3'
                elif colour == '#4d4dc4':
                    additional_multiplication += '*2'
                elif colour == '#6fcc45':
                    additional_point += '+' + str(self.count_letters_and_price[el[2]][1])
                elif colour == '#cfca42':
                    additional_point += '+' + str(self.count_letters_and_price[el[2]][1] * 2)
            all_summa = eval('(' + str(summa) + additional_point + ')' + additional_multiplication)
        if self.opening_words_focused is False:
            all_summa *= 2
            self.opening_words_focused = True
        if len(self.new_word_all_letters) == 7:
            all_summa += 15
        self.players[self.queue][1] += all_summa
        self.players[self.queue][0].setText(self.players[self.queue][0].text().split('\n')[0]
                                            + '\n' + str(self.players[self.queue][1]) + ' баллов')
        self.another_player_move()

    def changing_letters(self):
        self.skipping_move += 1
        s = [self.btn_choice[i].text() for i in self.all_letters_to_replace]
        for changing_letter in self.all_letters_to_replace:
            self.btn_choice[changing_letter].setEnabled(True)
            n = random.choice(self.alphabet)
            while n in s:
                n = random.choice(self.alphabet)
            self.count_letters_and_price[n][0] -= 1
            self.count_letters_and_price[self.players[self.queue][2][changing_letter]][0] += 1
            self.btn_choice[changing_letter].setText(n + '\n' + str(self.count_letters_and_price[n][1]))
            self.players[self.queue][2][changing_letter] = n
        self.all_letters_to_replace.clear()
        self.another_player_move()
        self.btn_check.setEnabled(True)

    def another_player_move(self):
        self.error.setText('')
        self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #f0f0f0}')
        if self.game_over() is False:
            i = 0
            for el in self.btn_choice:
                if el.isEnabled() is False:
                    el.setEnabled(True)
                    n = random.choice(self.alphabet)
                    self.count_letters_and_price[n][0] -= 1
                    self.players[self.queue][2][i] = n
                i += 1
            if self.queue < self.count_player - 1:
                self.queue += 1
            else:
                self.queue = 0
            i = 0
            for el in self.btn_choice:
                el.setText(self.players[self.queue][2][i] + '\n' + str(
                    self.count_letters_and_price[self.players[self.queue][2][i]][1]))
                i += 1
            self.number_of_remaining_letters.setText('Осталось букв: ' + str(self.print_number_of_remaining_letters()))
            self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #c6c6ec}')

    def statistic(self):
        # bd.show()
        self.hide()

    def closeEvent(self, event):
        self.unexpected_interrupts = 1
        self.game_over()

    sys.excepthook = lambda cls, exception, traceback: sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
