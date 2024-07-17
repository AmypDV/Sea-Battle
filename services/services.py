from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None, size=10):
        self._length = length
        self._tp = tp
        self.x = x
        self.y = y
        self.__size = size
        self._cells = [1] * length
        self._is_move = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value


    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def set_start_coords(self, x, y):
        self.x = x
        self.y = y

    def get_start_coords(self):
        return self.x, self.y

    def _get_ship_poles(self):
        if self._tp == 1:
            res = set((y, x) for y in range(max([0, self.y - 1]), min([self.__size, self.y + 2])) \
                   for x in range(max([0, self.x - 1]), min([self.__size, self.x + self._length + 1])))
        else:
            res = set((y, x) for y in range(max([0, self.y - 1]), min([self.__size, self.y + self._length + 1])) \
                   for x in range(max([0, self.x - 1]), min([self.__size, self.x + 2])))
        return res

    def _get_pole(self):
        if self._tp == 1:
            res = tuple([(self.y, x) for x in range(self.x, self.x + self._length)])
        else:
            res = tuple([(y, self.x) for y in range(self.y, self.y + self._length)])
        return res

    def is_collide(self, ship):
        if ship.x is None:
            return False
        return not set(self._get_pole()).isdisjoint(ship._get_ship_poles())

    def is_out_pole(self, size=10):
        if self._tp == 1:
            return True if self.x < 0 or self.x + self._length >= size else False
        else:
            return True if self.y < 0 or self.y + self._length >= size else False

    def move(self, go=1):
        if self._is_move:
            if self._tp == 1:
                self.x += go
            else:
                self.y += go

    def __getitem__(self, key):
        if not 0 <= key < self._length:
            raise ValueError(f'Длина корабля {self._length}')
        return self._cells[key]

    def __setitem__(self, key, value):
        if not 0 <= key < self._length:
            raise ValueError(f'Длина корабля {self._length}')
        if value not in (1, 2):
            raise ValueError('Значение должно быть либо 1, либо 2')
        self._cells[key] = value


class GamePole:
    def __init__(self, size=8):
        self._size = size
        self._ships = []

    def __is_collides(self, ship):
        return any([ship.is_collide(s) for s in self._ships if s != ship])

    def __get_xy(self, ship):
        if ship._tp == 1:
            x = randint(0, self._size - 1 - ship._length)
            y = randint(0, self._size - 1)
        else:
            x = randint(0, self._size - 1)
            y = randint(0, self._size - 1 - ship._length)
        return x, y

    def init(self):
        self._ships = []
        for n in range(3, 0, -1): # MAX ТРЕХЛИНЕЙНЫЙ
            for _ in range(5 - n):
                self._ships.append(Ship(n, randint(1, 2)))
        for ship in self._ships:
            ship.x, ship.y = self.__get_xy(ship)
            n = 0
            while ship.is_out_pole(self._size) or self.__is_collides(ship):
                n += 1
                ship.x, ship.y = self.__get_xy(ship)
                if n == 100000:
                    print('внимание 100000')
                    self.init()


    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship in self._ships:
            if ship._is_move:
                x = ship.x
                y = ship.y
                vector = choice([-1, 1])
                ship.move(vector)
                if ship.is_out_pole(self._size) or self.__is_collides(ship):
                    vector = [-2, 2][vector == -1]
                    ship.move(vector)
                    if ship.is_out_pole(self._size) or self.__is_collides(ship):
                        ship.x = x
                        ship.y = y

    def show(self):
        pole = self.get_pole()
        [print(*line) for line in pole]

    def get_pole(self):

        pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            if ship.x is not None and ship.y is not None:
                for y, x in ship._get_pole():
                    pole[y][x] = 1
        return tuple([tuple(i) for i in pole])



