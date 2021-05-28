# Эрудит

Эрудит - настольная игра, в которой от двух до четырёх играющих соревнуются в образовании слов с использованием буквенных деревянных плиток на доске, разбитой на 225 квадратов

## Содержание
* [Что такое "Эрудит"](#about)
* [Запуск проекта](#start)
* [Особенности реализации](#features)
***
***

> Проект работает на Python 3.8

### Правила игры "Эрудит" <a name="about"></a>

Игровое поле состоит из 15×15, то есть 225 квадратов, на которые участники игры выкладывают буквы, составляя тем самым слова.  В начале игры каждый игрок получает 7 случайных букв (всего их в игре 131). Через центральную клетку игрового поля по горизонтали или вертикали выкладывается первое слово, затем следующий игрок может добавить слово «на пересечение» из своих букв. Слова выкладываются либо слева направо, либо сверху вниз. Каждый игрок стремится выиграть игру, создавая больше слов на основе имеющихся костяшек с буквами.

##### Словарь

Разрешено использовать только литературные нарицательные имена существительные в именительном падеже единственного числа. Запрещается использовать словарь для поиска слов.


##### Игра

В начале игры каждому дается по 7 костяшек. За один ход можно составить несколько слов. Каждое новое слово должно соприкасаться или иметь общую букву (или буквы) с ранее составленными словами. Слова должны читаться слева направо (по горизонтали) и сверху вниз (по вертикали). Первое составленное слово должно проходить через центральную клетку. Если игрок не хочет или не может составить ни одного слова, — он имеет право поменять любое количество своих букв, пропустив при этом ход. («любое количество» может означать и ноль, то есть игрок имеет право просто пасовать, не меняя ни одной фишки). После каждого хода будет производиться добор новых букв до семи. Если за ход игрок использовал все семь косточек, то ему начисляются дополнительные 15 очков.
Игра заканчивается в следующих случаях:
когда у одного из игроков кончаются фишки на руках, и при этом нет больше фишек для добора (все они на руках или на поле);
когда все игроки последовательно пропустили ход два круга подряд.


##### Распределение фишек и стоимость букв

Каждой букве присвоено некоторое количество баллов от 1 до 10. Некоторые квадраты на доске раскрашены в разные цвета. Количество баллов, получаемых игроком за выложенное слово, подсчитывается следующим образом:

- если квадрат под буквой бесцветен, добавляется количество очков, написанное на букве
- если квадрат зелёный, количество очков буквы умножается на 2
- если квадрат синий, количество очков всего слова умножается на 2
- если квадрат жёлтый, количество очков буквы умножается на 3
- если квадрат красный, количество очков всего слова умножается на 3
- если слово пересекает и красную (синюю), и зелёную (жёлтую) клетки, то в утроении (удвоении) очков слова учитывается утроение (удвоение) очков букв.
- если слово пересекает две умножающих очки всего слова клетки, то учитываются обе операции. Например, если слово прошло через две красные клетки, то общий счёт очков слова умножается на 9.

> В данной реализации отсутствуют пустышки. Распределение баллов можете посмотреть на https://ru.wikipedia.org/wiki/%D0%A1%D0%BA%D1%80%D1%8D%D0%B1%D0%B1%D0%BB

##### Завершение игры 

Завершение игры происходит, если каждый игрок пропустит ход 2 раза подряд или если не осталось букв.

### Запуск проекта <a name="start"></a>
Перед запуском проекта установите дополнительные библиотеки указаные в requirements.txt

Далее запустите main.py. 
- В открывшемся окне в правом верхнем углу отметьте количество участников и введите их имена.
- Нажмите кнопку "Запомнить"

Игра началась.

### Особенности реализации <a name="features"></a>

- Для выстраивания слова на поле нужно перетащить одну из 7 букв. Далее также сохранится возможность перемещать буквы.
- Для того чтобы заменить буквы, их нужно перетащить в поле с соответсвующей надписью и нажать кнопку заменить.
- Статистику по играм и пользователям можно увидеть после завершения игры, нажав на кнопку "Статистика".
- Масштаб основного окна можно изменять.

