import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import pymorphy2
import random
import sqlite3
from DBSample import DataBase
from design.design import Ui_MainWindow

SIZE_FIELD = 15


class MovableButton(QPushButton):
    # отвечает за буквы из которых игроки составляют слова
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if type(e.source()) == Button and self.styleSheet()[31:-1] == '#c6c6ec' and \
                self.text() == e.source().text():
            self.setStyleSheet('QPushButton {background-color:"white"; color:"black"}')
            e.source().setText('')
            e.setDropAction(Qt.MoveAction)
            e.accept()
            main_window.used_letters.remove(self)
            if not len(main_window.used_letters):
                main_window.replaced_letters.setEnabled(True)
                main_window.btn_replaced_letters.setEnabled(True)
            main_window.btn_letters_of_new_words.remove(e.source())


class ButtonToReplaceTheLetters(QPushButton):
    # место для скидывания букв, которые надо заменить
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if type(e.source()) == MovableButton:
            e.source().setStyleSheet('QPushButton {background-color: #c6c6ec}')
            # в letters_to_replace хранятся кнопки
            main_window.letters_to_replace.append(e.source())
            main_window.btn_check.setEnabled(False)
            e.setDropAction(Qt.MoveAction)
            e.accept()


class Button(QPushButton):
    # клетки поля
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if self.text() == '' and type(e.source()) == MovableButton:
            main_window.replaced_letters.setEnabled(False)
            main_window.btn_replaced_letters.setEnabled(False)
            self.setText(e.mimeData().text())
            e.source().setStyleSheet('QPushButton {background-color: #c6c6ec}')
            e.setDropAction(Qt.MoveAction)
            e.accept()
            main_window.btn_letters_of_new_words.append(self)
            main_window.used_letters.append(e.source())
        if self.text() == '' and type(e.source()) == Button:
            e.source().setText('')
            self.setText(e.mimeData().text())
            e.setDropAction(Qt.MoveAction)
            e.accept()
            if e.source() in main_window.btn_letters_of_new_words:
                main_window.btn_letters_of_new_words.remove(e.source())
            main_window.btn_letters_of_new_words.append(self)

    def mouseMoveEvent(self, e):
        if self.isEnabled():
            mimeData = QMimeData()
            mimeData.setText(self.text())
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos() - self.rect().topLeft())
            dropAction = drag.exec_(Qt.MoveAction)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Загружаем дизайн
        self.initUI()

    def initUI(self):
        self.btn_letters_of_new_words = []
        self.words_used_in_the_game = []
        self.statistics.clicked.connect(self.statistic)
        self.statistics.show()
        self.new_play.hide()
        self.new_play.clicked.connect(self.new_play_start)
        self.price_letters = {'А': 1, 'Б': 3, 'В': 2, 'Г': 3, 'Д': 2, 'Е': 1, 'Ж': 5, 'З': 5,
                              'И': 1, 'Й': 2, 'К': 2, 'Л': 2, 'М': 2, 'Н': 1, 'О': 1, 'П': 2,
                              'Р': 2, 'С': 2, 'Т': 2, 'У': 3, 'Ф': 10, 'Х': 5, 'Ц': 10, 'Ч': 5,
                              'Ш': 10, 'Щ': 10, 'Ъ': 10, 'Ы': 5, 'Ь': 5, 'Э': 10, 'Ю': 10, 'Я': 3}
        self.alphabet = ['А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'Б', 'Б', 'Б', 'В', 'В',
                         'В', 'В', 'В', 'Г', 'Г', 'Г', 'Д', 'Д', 'Д', 'Д', 'Д', 'Е', 'Е', 'Е', 'Е',
                         'Е', 'Е', 'Е', 'Е', 'Е', 'Ж', 'Ж', 'З', 'З', 'И', 'И', 'И', 'И', 'И', 'И',
                         'И', 'И', 'Й', 'Й', 'Й', 'Й', 'К', 'К', 'К', 'К', 'К', 'К', 'Л', 'Л', 'Л',
                         'Л', 'М', 'М', 'М', 'М', 'М', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'О',
                         'О', 'О', 'О', 'О', 'О', 'О', 'О', 'О', 'О', 'П', 'П', 'П', 'П', 'П', 'П',
                         'Р', 'Р', 'Р', 'Р', 'Р', 'Р', 'С', 'С', 'С', 'С', 'С', 'С', 'Т', 'Т', 'Т',
                         'Т', 'Т', 'У', 'У', 'У', 'Ф', 'Х', 'Х', 'Ц', 'Ч', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
                         'Ы', 'Ь', 'Ь', 'Э', 'Ю', 'Я', 'Я', 'Я']
        self.setGeometry(200, 30, 800, 600)
        self.btn_check.clicked.connect(self.check)
        self.first_word_created = False
        self.replaced_letters = ButtonToReplaceTheLetters('Скинте сюда буквы,\n которые'
                                                          ' нужно заменить', self)
        self.gridLayout.addWidget(self.replaced_letters, 13, 1, 1, 1)
        self.replaced_letters.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_replaced_letters.clicked.connect(self.changing_letters)
        self.field = [['' for _ in range(SIZE_FIELD)] for __ in range(SIZE_FIELD)]
        self.used_letters = []
        self.queue = 0
        self.skipping_move = 0
        self.unexpected_interrupt = 0
        self.change_bd = 0
        for i in range(4):
            eval(f'self.player{i + 1}.hide()')
        # создаем поле
        for j in range(SIZE_FIELD):
            for i in range(SIZE_FIELD):
                name = Button('', self)
                name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                # раскрашиваем поле
                if i == j or i + j == SIZE_FIELD - 1:
                    if i == 0 or i == SIZE_FIELD - 1:
                        name.setStyleSheet('QPushButton {background-color: #c4544d}')
                    elif 1 <= i <= 4 or 10 <= i <= 13:
                        name.setStyleSheet('QPushButton {background-color: #4d4dc4}')
                    elif i == 6 or i == 8:
                        name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i + j == 10 or i - j == 4:
                    if j == 1 or j == 9:
                        name.setStyleSheet('QPushButton {background-color: #cfca42}')
                    elif j == 2 or j == 3 or j == 7 or j == 8:
                        name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i + j == 18 or j - i == 4:
                    if j == 5 or j == 13:
                        name.setStyleSheet('QPushButton {background-color: #cfca42}')
                    elif j == 6 or j == 7 or j == 11 or j == 12:
                        name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                elif i == 0 or i == SIZE_FIELD - 1:
                    if j == 3 or j == 11:
                        name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                    elif j == 7:
                        name.setStyleSheet('QPushButton {background-color: #c4544d}')
                elif j == 0 or j == SIZE_FIELD - 1:
                    if i == 3 or i == 11:
                        name.setStyleSheet('QPushButton {background-color: #6fcc45}')
                    elif i == 7:
                        name.setStyleSheet('QPushButton {background-color: #c4544d}')
                self.grid_field.addWidget(name, i + 1, j + 1)
        for i in range(2, 4):
            eval(f'self.name{i + 1}.hide()')
        self.btn_choice = []
        self.players = []
        self.btn_remember.clicked.connect(self.remember)
        for i in range(2, 4):
            eval(f'self.checkBox_{i + 1}.stateChanged.connect(self.player_added)')
        self.count_player = 2
        # создаем передвижимые кнопки
        for i in range(7):
            name = MovableButton('', self)
            # self.name.setMinimumSize(35, 35)
            name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            name.setStyleSheet('QPushButton {background-color:"white"; color:"black"}')
            self.grid_field.addWidget(name, 16, i + 1)
            name.hide()
            self.btn_choice.append(name)

    def player_added(self):
        self.count_player = 0
        for i in range(4):
            if eval(f'self.checkBox_{i + 1}.isChecked()'):
                eval(f'self.name{i + 1}.show()')
                self.count_player += 1
            else:
                eval(f'self.name{i + 1}.hide()')

    def remember(self):
        for el in self.btn_choice:
            el.show()
        if not (eval(f'self.checkBox_3.isChecked()')) and self.count_player == 3:
            self.statusBar().showMessage(f'Игроки должны регестрироваться по порядку. '
                                         f'Не оставляйте пустых мест. Попробуйте снова.')
            self.statusBar().setStyleSheet("background-color:red;")
            return
        self.statusBar().setStyleSheet("background-color:white;")
        self.statusBar().showMessage('')
        self.players = []
        self.btn_check.setEnabled(True)
        self.btn_replaced_letters.setEnabled(True)
        self.replaced_letters.setEnabled(True)
        # проходимся по всем игрокам и генерируем для каждого буквы
        for i in range(self.count_player):
            eval(f"self.player{i + 1}").setText(eval(f"self.name{i + 1}.text()") + '\n 0 баллов')
            s = []
            for j in range(7):
                n = random.choice(self.alphabet)
                self.alphabet.remove(n)
                s.append(n)
            self.players.append([eval(f'self.player{i + 1}'), 0, s])
        i = 0
        # заполняем кнопки буквами игрока, который будет первым ходить
        for el in self.btn_choice:
            el.setText(self.players[self.queue][2][i] + '\n' + str(
                self.price_letters[self.players[self.queue][2][i]]))
            i += 1
        self.letters_to_replace = []
        self.number_of_remaining_letters.setText(
            'Осталось букв: ' + str(len(self.alphabet)))
        self.skipping_move = 0
        # скрываем регистрационное поле
        self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #c6c6ec}')
        for i in range(4):
            eval(f'self.name{i + 1}.hide()')
            eval(f'self.checkBox_{i + 1}.hide()')
        self.label.setText('')
        self.btn_remember.hide()
        for i in range(self.count_player):
            eval(f'self.player{i + 1}.show()')

    def game_over(self):
        if len(self.alphabet) == 0 or self.skipping_move == self.count_player * 2 \
                or self.unexpected_interrupt:
            if self.change_bd == 0:
                self.change_bd = 1
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
                self.statusBar().showMessage('Игра окончена! Ничья!')
            else:
                self.statusBar().showMessage(
                    'Игра окончена! Наибольшее количество баллов набрали: ' +
                    ', '.join(el[0] for el in maxim_name))
            self.statusBar().setStyleSheet("background-color:orange;")
            self.add_winner_in_bd(maxim_name)
            self.btn_check.hide()
            self.btn_replaced_letters.hide()
            self.replaced_letters.hide()
            self.new_play.show()
            for el in self.btn_choice:
                el.hide()
            return True
        return False

    def new_play_start(self):
        self.statusBar().setStyleSheet("background-color:white;")
        self.statusBar().showMessage('')
        for i in range(SIZE_FIELD):
            for j in range(SIZE_FIELD):
                button = self.grid_field.itemAtPosition(i + 1, j + 1).widget()
                button.setText('')
                button.setEnabled(True)
        self.alphabet = ['А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'А', 'Б', 'Б', 'Б', 'В', 'В',
                         'В', 'В', 'В', 'Г', 'Г', 'Г', 'Д', 'Д', 'Д', 'Д', 'Д', 'Е', 'Е', 'Е', 'Е',
                         'Е', 'Е', 'Е', 'Е', 'Е', 'Ж', 'Ж', 'З', 'З', 'И', 'И', 'И', 'И', 'И', 'И',
                         'И', 'И', 'Й', 'Й', 'Й', 'Й', 'К', 'К', 'К', 'К', 'К', 'К', 'Л', 'Л', 'Л',
                         'Л', 'М', 'М', 'М', 'М', 'М', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'Н', 'О',
                         'О', 'О', 'О', 'О', 'О', 'О', 'О', 'О', 'О', 'П', 'П', 'П', 'П', 'П', 'П',
                         'Р', 'Р', 'Р', 'Р', 'Р', 'Р', 'С', 'С', 'С', 'С', 'С', 'С', 'Т', 'Т', 'Т',
                         'Т', 'Т', 'У', 'У', 'У', 'Ф', 'Х', 'Х', 'Ц', 'Ч', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
                         'Ы', 'Ь', 'Ь', 'Э', 'Ю', 'Я', 'Я', 'Я']
        self.field = [['' for _ in range(SIZE_FIELD)] for __ in range(SIZE_FIELD)]
        self.first_word_created = False
        self.remember()
        self.change_bd = 0
        self.btn_check.show()
        self.btn_replaced_letters.show()
        self.replaced_letters.show()
        self.new_play.hide()

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

    def new_words(self):
        letters = []
        for i in range(len(self.btn_letters_of_new_words)):
            position = self.grid_field.getItemPosition(
                self.grid_field.indexOf(self.btn_letters_of_new_words[i]))
            self.field[position[0] - 1][position[1] - 1] = \
                self.btn_letters_of_new_words[i].text().split('\n')[0]
            letters.append(
                (position[0] - 1, position[1] - 1,
                 self.btn_letters_of_new_words[i].text().split('\n')[0]))
        all_word = []
        words_buttons = []
        for el in letters:
            n = 1
            index_x_upper, index_y_upper = el[0], el[1]
            index_x_lower, index_y_lower = el[0], el[1]
            x, y = el[0], el[1]
            while n:
                n = 4
                if index_x_upper > 0 and self.field[index_x_upper - 1][y] != '':
                    index_x_upper -= 1
                else:
                    n -= 1
                if index_x_lower < SIZE_FIELD - 1 and self.field[index_x_lower + 1][y] != '':
                    index_x_lower += 1
                else:
                    n -= 1
                if index_y_upper > 0 and self.field[x][index_y_upper - 1] != '':
                    index_y_upper -= 1
                else:
                    n -= 1
                if index_y_lower < SIZE_FIELD - 1 and self.field[x][index_y_lower + 1]:
                    index_y_lower += 1
                else:
                    n -= 1
            word = ''
            word_buttons = []
            for i in range(index_x_upper, index_x_lower + 1):
                word_buttons.append(self.grid_field.itemAtPosition(i + 1, y + 1).widget())
                word += self.field[i][y]
            if len(word) > 1 and not (word in all_word):
                words_buttons.append(word_buttons)
                all_word.append(word)
            word = ''.join(self.field[x][index_y_upper:index_y_lower + 1])
            if len(word) > 1 and not (word in all_word):
                words_buttons.append([self.grid_field.itemAtPosition(x + 1, i + 1).widget()
                                      for i in range(index_y_upper, index_y_lower + 1)])
                all_word.append(word)
        return all_word, words_buttons

    def check_the_existence_of_the_word(self, word):
        # проверка на существование слова
        analysis = pymorphy2.MorphAnalyzer().parse(word)[:2]
        if pymorphy2.MorphAnalyzer().word_is_known(word):
            for el in analysis:
                if el.tag.POS == 'NOUN' and 'nomn' in el.tag and \
                        (el.tag.number == 'sing') and 'Name' not in el.tag:
                    return True
        return False

    def clear_field(self):
        for word in self.btn_letters_of_new_words:
            word.setText('')
            position = self.grid_field.getItemPosition(self.grid_field.indexOf(word))
            self.field[position[0] - 1][position[1] - 1] = ''
        for button in self.used_letters:
            button.setStyleSheet('QPushButton {background-color:"white"; color:"black"}')
        self.btn_letters_of_new_words.clear()
        self.used_letters.clear()

    def check(self):
        self.btn_replaced_letters.setEnabled(True)
        self.replaced_letters.setEnabled(True)
        new_words, words_buttons = self.new_words()
        if not len(new_words):
            self.statusBar().showMessage(f'Слов не найдено. Попробуйте снова.')
            self.statusBar().setStyleSheet("background-color:red;")
            self.clear_field()
            return
        if not self.first_word_created and self.field[SIZE_FIELD // 2][SIZE_FIELD // 2] == '':
            self.statusBar().showMessage(
                f'Первое слово должно проходить через середину поля. Попробуйте снова.')
            self.statusBar().setStyleSheet("background-color:red;")
            self.clear_field()
            return
        if len(new_words) == 0 and len(self.used_letters) > 0:
            self.statusBar().showMessage(
                f'Слова состоящие из одной буквы не считаются! Попробуйте снова.')
            self.statusBar().setStyleSheet("background-color:red;")
            self.clear_field()
            return
        len_buttons = sum(len(el) for el in words_buttons)
        for i in range(len(new_words)):
            if not self.check_the_existence_of_the_word(new_words[i]):
                self.statusBar().showMessage(f'О слове "{new_words[i]}" я никогда не слышал'
                                             f'! Придумайте что-нибудь другое.')
                self.statusBar().setStyleSheet("background-color:red;")
                self.clear_field()
                return
            if all(el in self.btn_letters_of_new_words for el in words_buttons[i]) and \
                    len(self.btn_letters_of_new_words) == len_buttons and self.first_word_created:
                self.statusBar().showMessage(f'Слово "{new_words[i]}" не соприкасается '
                                             f'с остальными словами! Попробуйте снова.')
                self.statusBar().setStyleSheet("background-color:red;")
                self.clear_field()
                return
            if new_words[i] in self.words_used_in_the_game:
                self.statusBar().showMessage(f'Слово "{new_words[i]}" уже было! Попробуйте снова.')
                self.statusBar().setStyleSheet("background-color:red;")
                self.clear_field()
                return
        for el in self.btn_letters_of_new_words:
            # el.setStyleSheet('QPushButton {background-color: #f0f0f0}')
            el.setEnabled(False)
        self.words_used_in_the_game.extend(new_words)
        self.scoring_points(words_buttons)
        self.btn_letters_of_new_words.clear()
        self.another_player_move()
        self.used_letters.clear()

    def scoring_points(self, new_words_buttons):
        # считет баллы за слова
        summa, all_summa = 0, 0
        additional_point = ''
        additional_multiplication = ''
        for word in new_words_buttons:
            for el in word:
                colour = el.styleSheet()[31:-1]
                el = el.text().split('\n')[0]
                summa += self.price_letters[el]
                if colour == '#c4544d':
                    additional_multiplication += '*3'
                elif colour == '#4d4dc4':
                    additional_multiplication += '*2'
                elif colour == '#6fcc45':
                    additional_point += '+' + str(self.price_letters[el])
                elif colour == '#cfca42':
                    additional_point += '+' + str(self.price_letters[el] * 2)
                all_summa = eval(
                    '(' + str(summa) + additional_point + ')' + additional_multiplication)
        if not self.first_word_created:
            all_summa *= 2
            self.first_word_created = True
        if len(self.used_letters) == 7:
            all_summa += 15
        self.players[self.queue][1] += all_summa
        self.players[self.queue][0].setText(self.players[self.queue][0].text().split('\n')[0]
                                            + '\n' + str(self.players[self.queue][1]) + ' баллов')

    def changing_letters(self):
        self.skipping_move += 1
        s = [i.text() for i in self.letters_to_replace]
        for changing_letter in self.letters_to_replace:
            changing_letter.setStyleSheet('QPushButton {background-color:"white"; color:"black"}')
            n = random.choice(self.alphabet)
            while n in s:
                n = random.choice(self.alphabet)
            self.alphabet.remove(n)
            position = self.grid_field.getItemPosition(self.grid_field.indexOf(changing_letter))
            self.alphabet.append(self.players[self.queue][2][position[1] - 1])
            changing_letter.setText(n + '\n' + str(self.price_letters[n]))
            self.players[self.queue][2][position[1] - 1] = n
        self.letters_to_replace.clear()
        self.another_player_move()
        self.btn_check.setEnabled(True)

    def another_player_move(self):
        self.statusBar().setStyleSheet("background-color:white;")
        self.statusBar().showMessage('')
        self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #f0f0f0}')
        if self.game_over() is False:
            for el in self.used_letters:
                el.setStyleSheet('QPushButton {background-color:"white"; color:"black"}')
                n = random.choice(self.alphabet)
                self.alphabet.remove(n)
                position = self.grid_field.getItemPosition(self.grid_field.indexOf(el))
                self.players[self.queue][2][position[1] - 1] = n
            if self.queue < self.count_player - 1:
                self.queue += 1
            else:
                self.queue = 0
            i = 0
            for el in self.btn_choice:
                el.setText(self.players[self.queue][2][i] + '\n' + str(
                    self.price_letters[self.players[self.queue][2][i]]))
                i += 1
            self.number_of_remaining_letters.setText(
                'Осталось букв: ' + str(len(self.alphabet)))
            self.players[self.queue][0].setStyleSheet('QPushButton {background-color: #c6c6ec}')

    def statistic(self):
        db.show()
        self.hide()

    def closeEvent(self, event):
        self.unexpected_interrupt = 1
        self.game_over()

    sys.excepthook = lambda cls, exception, traceback: sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    db = DataBase(main_window)
    db.hide()
    sys.exit(app.exec())
