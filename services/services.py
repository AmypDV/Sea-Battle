from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None, size=8):
        self._length = length
        self._tp = tp
        self.x = x
        self.y = y
        self.__size = size
        self.cells: dict[tuple[int, int], int] = {}
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

    def set_start_xy(self, x, y):
        self.cells = {}
        self.x = x
        self.y = y
        for tuple_of_xy in self._get_pole():
            self[tuple_of_xy] = 1

    def get_start_coords(self):
        return self.y, self.x

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
            res = tuple((self.y, x) for x in range(self.x, self.x + self._length))
        else:
            res = tuple((y, self.x) for y in range(self.y, self.y + self._length))
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
        if key not in self._get_pole():
            raise ValueError('Корабль не плавает в этих водах')
        return self.cells[key]

    def __setitem__(self, key, value):
        if key not in self._get_pole():
            raise ValueError('Корабль не плавает в этих водах')
        if value not in (1, 2):
            raise ValueError('Значение должно быть либо 2 - подбитая часть корабля, либо 1 - целая часть')
        self.cells[key] = value


class GamePole:
    def __init__(self, size=8):
        self._size = size
        self._ships = []
        self._hits = []
        self._all_cells: list[tuple[int, int]] = []

    def set_hit(self, hit:tuple):
        self._hits.append(hit)

    def __is_collides(self, ship):

        return any([ship.is_collide(s) for s in self._ships if s != ship])

    def __get_start_xy(self, ship):
        if ship._tp == 1:
            x = randint(0, self._size - 1 - ship._length)
            y = randint(0, self._size - 1)
        else:
            x = randint(0, self._size - 1)
            y = randint(0, self._size - 1 - ship._length)
        return x, y

    def init(self):
        self._ships = []
        self._all_cells = []
        for n in range(3, 0, -1): # MAX ТРЕХЛИНЕЙНЫЙ 
            for _ in range(5 - n):
                self._ships.append(Ship(n, randint(1, 2), size=self._size))
        for ship in self._ships:
            x, y = self.__get_start_xy(ship)
            ship.set_start_xy(x, y)
            n = 0
            while self.__is_collides(ship):
                n += 1
                x, y = self.__get_start_xy(ship)
                ship.set_start_xy(x, y)
                if n == 100000:
                    print('внимание 100000')  # Слишком много попыток  -> начинаем сначала
                    self.init()
            [self._all_cells.append(cell) for cell in ship.cells.keys()]


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
        '''
        Создается поле в котором:
        0 - пустое поле
        1 - находится корабль
        2 - находится подбитая часть корабля
        3 - промах
        '''
        pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            if ship.x is not None and ship.y is not None:
                for coords, value in ship.cells.items():
                    y, x = coords
                    pole[y][x] = value

        for cords in self._hits:
            y, x = cords
            pole[y][x] = 3
        return tuple([tuple(i) for i in pole])

    def hit(self, *yx):
        if yx in self._all_cells:
            for ship in self._ships:
                if yx in ship.cells: # попадание в корабль
                    if ship[yx] == 1:
                        ship[yx] = 2
                        if all(all(map(lambda x: x == 2, s.cells.values())) for s in self._ships):
                            return 'victory'
                        if all(map(lambda x: x == 2, ship.cells.values())): # потопил
                            return 'sunk'
                        else:
                            return 'hit'
                    else:
                        return 'already_fight'
        else:
            if yx in self._hits: # стреляли в это поле
                return 'already_fight'
            else:
                self._hits.append(yx)
                return 'miss'





