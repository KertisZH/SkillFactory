import time

from random import randint


DIVIDER = '-----------------------------------------'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за пределы поля боя!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в этот сектор!'


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, ship_bow, length, orientation):
        self.ship_bow = ship_bow  # нос корабля
        self.length = length  # длина корабля
        self.orientation = orientation  # ориентация корабля (вертикально/горизонтально)
        self.lives = length  # количество оставшихся попаданий

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.ship_bow.x  # координата носа корабля по горизонтали
            cur_y = self.ship_bow.y  # координата носа корабля по вертикали

            if self.orientation == 0:  # 0 - горизонтальная ориентация корабля
                cur_x += i

            elif self.orientation == 1:  # 1 - вертикальная ориентация корабля
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    # Этот метод нигде не используется?
    # def shot(self, shot):
    #     return shot in self.dots


class Board:
    def __init__(self, hide_board=False, size=6):  # установленный размер поля: 6х6.
        self.size = size
        self.hide_board = hide_board

        self.dead_ships = 0

        self.field = [['O'] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'  # символ которым отображается корабль
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def print_header(self):
        return '  | 1 | 2 | 3 | 4 | 5 | 6 |'

    def print_row(self, row_num):
        res = f'{row_num + 1} | ' + ' | '.join(self.field[row_num]) + ' |'
        if self.hide_board:
            res = res.replace('■', 'O')

        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.dead_ships += 1
                    self.contour(ship, verb=True)
                    print('Корабль потоплен!')
                    return False
                else:
                    print('Корабль повреждён!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()  # реализация этого метода зависит от подкласса

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))  # диапазон (0, 5) при размере игрового поля 6х6.
        print(f'Сейчас ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input('Сейчас Ваш ход: ').split()
            if len(coords) != 2:
                print(' Введите 2 координаты! ')
                continue

            x, y = coords

            if not (x.isdigit()) or not (y.isdigit()):
                print(' Введите числа! ')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide_board = True

        self.computer = AI(co, pl)
        self.player = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]  # размеры кораблей
        board = Board(size=self.size)
        attempts = 0
        for length in lens:
            while True:
                attempts += 1
                if attempts > 30:  # максимальное теоретическое количество попыток уж никак не 2000
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    @staticmethod  # в этом методе не используются свойства объекта, поэтому self здесь не нужен
    def greet():
        print(DIVIDER)
        print('   Приветсвуем вас в игре морской бой')
        print(DIVIDER)
        print(' формат ввода: x y')
        print(' x - номер строки')
        print(' y - номер столбца')
        print(DIVIDER)

    def print_boards(self):
        second_board_offset = 2 * '\t'  # расстояние между досками равно двум табуляциям
        print('         PLAYER                            COMPUTER')
        print(self.player.board.print_header() + second_board_offset + self.computer.board.print_header())
        for i in range(self.size):
            print(self.player.board.print_row(i) + second_board_offset + self.computer.board.print_row(i))

    def loop(self):
        num = 0
        while True:
            self.print_boards()

            repeat_player = False
            repeat_computer = False
            if num % 2 == 0:
                print('-' * 20)
                print('Сейчас ходит пользователь!')
                repeat_player = self.player.move()
            else:
                print('-' * 20)
                print('Сейчас ходит компьютер!')
                repeat_computer = self.computer.move()

            if repeat_player:
                num -= 1
            elif repeat_computer:
                time.sleep(1)  # компьютер задумался
                print('Компьютер думает как победить человеков!!!')

            if self.computer.board.dead_ships == 7:
                print('-' * 20)
                print('Пользователь выиграл!')
                break

            if self.player.board.dead_ships == 7:
                print('-' * 20)
                print('Компьютер выиграл! Мы убъём всех человеков!!! (С) Бендер')
                break

            num += 1

        self.print_boards()

    def start(self):
        self.greet()
        self.loop()

try:
    g = Game()
    g.start()
except BaseException:
    print('Возникла непредвиденная ситуация!')
