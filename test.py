class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class BoardExecption(Exception):
    pass


class BoardOutExecption(BoardExecption):
    def __str__(self):
        return "Вы вышли за координаты доски!"


class BoardUsedExecption(BoardExecption):
    def __str__(self):
        return "Вы уже стреляли в эту точку"


class BoardWrongShipException(BoardExecption):
    pass
# a = Dot(1, 2)
# b = Dot(1, 3)
# print(a)
# print(a==b)

# cc = [Dot(2,4), Dot(5,2), Dot(1,4),Dot(1,3), Dot(2,2)]
# print(a in cc)

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l  #############

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


#s = Ship(Dot(1, 1), 4, 0)
#print(s.dots)
#print(s.shooten(Dot(2, 1)))

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size+1)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 0 | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
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
                #self.field[cur.x][cur.y] = "+"
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ships(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardBoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contur(ship)
g = Board()
g.add_ships(Ship(Dot(2, 2), 4, 0))
g.add_ships(Ship(Dot(0, 0), 1, 0))

print(g)
