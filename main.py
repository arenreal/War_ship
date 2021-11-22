from random import randint
import time



# Execption
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы вышли за пределы доски!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot[{self.x}, {self.y}]'


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shoot):
        return shoot in self.dots




class Board:

    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.count = 0
        self.field = [["О"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"

        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "О")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contur(self, ship, verb=False):

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
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contur(ship)

    def shoot(self,d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contur(ship, verb=True)
                    print("\n")
                    print("Корабль уничтожен!")
                    print(input("Нажмите Enter, чтобы продолжить"))
                    return True
                else:
                    print("Корабль ранен!")
                    print(input("Нажмите Enter, чтобы продолжить"))
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        print(input("Нажмите Enter, чтобы продолжить"))
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as e:
                print(e)
class Ai(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f"Ход компьютера: {d.x +1},{d.y +1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Введите Ваши координаты: ").split()

            if len(cords) != 2:
                print("Введите две координаты: ")
                continue
            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)

class Game:
    def __init__(self, size =6):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = Ai(co,pl)
        self.us = User(pl,co)

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-"*40)
        print("         Добро пожаловать  ")
        print("              в игру       ")
        print("            морской бой    ")
        print("-" * 40)
        print("     Формат ввода кооординат: x y ")
        print("         x - номер строки  ")
        print("         y - номер столбца ")
        print("     Поврежденные места на корабле ")
        print("         обозначаются как 'X '  ")
        print("     Места промаха обозначаются как '.' ")
    def loop(self):
        num = 0
        while True:
            print("-"*40)
            print("Ваша игровая доска")
            print(self.us.board)
            print("Доска противника")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 ==0:
                print("Ваш ход")
                repeat = self.us.move()
            else:
                print("Компьютер думает....")
                time.sleep(3)
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.defeat():
                print("-" * 20)
                print("ВЫ ВЫИГРАЛИ!")
                print(""" .
                ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                ⠄⠄⠄⠄⣠⠞⠉⢉⠩⢍⡙⠛⠋⣉⠉⠍⢉⣉⣉⣉⠩⢉⠉⠛⠲⣄⠄⠄⠄⠄
                ⠄⠄⠄⡴⠁⠄⠂⡠⠑⠄⠄⠄⠂⠄⠄⠄⠄⠠⠄⠄⠐⠁⢊⠄⠄⠈⢦⠄⠄⠄
                ⠄⣠⡾⠁⠄⠄⠄⣴⡪⠽⣿⡓⢦⠄⠄⡀⠄⣠⢖⣻⣿⣒⣦⠄⡀⢀⣈⢦⡀⠄
                ⣰⠑⢰⠋⢩⡙⠒⠦⠖⠋⠄⠈⠁⠄⠄⠄⠄⠈⠉⠄⠘⠦⠤⠴⠒⡟⠲⡌⠛⣆
                ⢹⡰⡸⠈⢻⣈⠓⡦⢤⣀⡀⢾⠩⠤⠄⠄⠤⠌⡳⠐⣒⣠⣤⠖⢋⡟⠒⡏⡄⡟
                ⠄⠙⢆⠄⠄⠻⡙⡿⢦⣄⣹⠙⠒⢲⠦⠴⡖⠒⠚⣏⣁⣤⣾⢚⡝⠁⠄⣨⠞⠄
                ⠄⠄⠈⢧⠄⠄⠙⢧⡀⠈⡟⠛⠷⡾⣶⣾⣷⠾⠛⢻⠉⢀⡽⠋⠄⠄⣰⠃⠄⠄
                ⠄⠄⠄⠄⠑⢤⡠⢂⠌⡛⠦⠤⣄⣇⣀⣀⣸⣀⡤⠼⠚⡉⢄⠠⣠⠞⠁⠄⠄⠄
                ⠄⠄⠄⠄⠄⠄⠉⠓⠮⣔⡁⠦⠄⣤⠤⠤⣤⠄⠰⠌⣂⡬⠖⠋⠄⠄⠄⠄⠄⠄
                ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠒⠤⢤⣀⣀⡤⠴⠒⠉⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                """)
                print(input("Далее....(Нажмите Enter, чтобы увидеть доски!!)"))
                print(self.us.board)
                print(self.ai.board)
                break

            if self.us.board.defeat():
                print("-" * 20)
                print("-" * 20)
                print("Компьютер выиграл!")
                print("""
                .
⠟⠛⠉⠉⠉⠉⠉⠉⠙⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠻⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢻⣿⣿⣿⣿
⠄⠄⠄⠄⠄⢀⣀⣀⣀⣀⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿
⠄⠄⠄⠉⠉⠉⠄⣀⣀⣀⡈⠉⠛⠛⠛⠉⠉⠲⠄⠄⠄⣿⣿⣿
⠠⠤⠤⠔⠒⠋⠉⠄⠄⠄⠈⠉⠒⠒⠒⠒⠒⠂⠄⠄⠄⢻⣿⣿
⠄⠄⢀⠤⠐⠒⠒⠒⠒⠂⠄⠄⠄⠄⠄⠐⠒⠒⠒⢄⠄⠄⢿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠆⠄⠄⠄⠄⢰⠄⠄⠄⠄⠄⠄⢸⣿
⠄⠄⠄⢠⡖⢲⣶⣶⣤⡀⠄⠄⠄⠄⠄⠈⢀⣤⣤⣤⡀⠄⢸⣿
⠄⠄⠄⠈⠙⠚⠛⠛⠓⠃⠄⠄⠄⠄⠄⠄⠧⠤⢿⣿⡇⠄⢸⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢰⡆⠄⠄⠄⠄⠄⠄⠄⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠳⡀⠄⠄⠄⠄⠄⠄⢸
⠄⠄⠄⠄⠄⠄⠄⠄⠄⡤⠤⠄⠄⠄⠄⠄⢘⡆⠄⠄⠄⠄⢠⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠻⣤⠄⠴⠆⠠⣄⡞⠄⠄⠄⠄⢀⣾⣿
⣆⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣾⣿⣿
⠈⠳⣄⠄⠄⠄⠄⠄⠖⠒⠶⠤⠤⠤⠤⠤⢤⠄⠄⢀⣿⣿⣿⣿
⠄⠄⠈⠑⢦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣼⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠙⢦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⣠⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠈⠓⠲⠤⠤⠤⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠣⡀⠄⠄⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠉⠉⠉⠉⠉⠛⠛
⠄⠄⠈⠉⠑⢆⣀⡔⠈⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                """)
                print(input("Далее....(Нажмите Enter, чтобы увидеть доски!!)"))
                print(self.us.board)
                print(self.ai.board)
                break
            num += 1
    def start(self):
        self.greet()
        print(input("Далее....(Нажмите Enter)"))

        self.loop()

g = Game()
g.start()
