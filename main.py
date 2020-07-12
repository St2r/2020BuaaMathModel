import numpy as np
import matplotlib.pyplot as plt


class Person:
    def __init__(self, pos: tuple, direction: int = 0):
        self.x, self.y = pos
        self.direction = direction
        self.end = 0

    def target(self, k: int) -> tuple:
        switch = {
            0: (self.x, self.y),
            1: (self.x, self.y - 1),
            2: (self.x + 1, self.y - 1),
            3: (self.x + 1, self.y),
            4: (self.x + 1, self.y + 1),
            5: (self.x, self.y + 1),
            6: (self.x - 1, self.y + 1),
            7: (self.x - 1, self.y),
            8: (self.x - 1, self.y - 1),
        }
        return switch[k]

    def move(self, k: int):
        self.direction = k
        self.x, self.y = self.target(k)

    def getDistance(self, person):
        return pow(pow(self.x - person.x, 2) + pow(self.y - person.y, 2), 0.5)


class Exit:
    def __init__(self, pos: tuple):
        self.x, self.y = pos

    def getDistance(self, person: Person, k: int = 0):
        return pow(pow(self.x - person.target(k)[0], 2) + pow(self.y - person.target(k)[1], 2), 0.5)


class Obstacle:
    def __init__(self, point1: tuple, point2: tuple):
        if point1[0] < point2[0]:
            self.x1 = point1[0]
            self.x2 = point2[0]
        else:
            self.x1 = point2[0]
            self.x2 = point1[0]

        if point1[1] < point2[1]:
            self.y1 = point1[1]
            self.y2 = point2[1]
        else:
            self.y1 = point2[1]
            self.y2 = point1[1]

    # 判断位置是否在障碍物以内
    def contains(self, pos: tuple) -> bool:
        if self.x1 < pos[0] < self.x2 and self.y1 < pos[1] < self.y2:
            return True
        else:
            return False


class CA:
    def __init__(self, size: tuple):
        self._size = size
        self._map = np.zeros(size)
        self.hot_map = np.zeros(size)
        self.personList = list()
        self.exitList = list()
        self.obstacleList = list()
        self.fig = plt.matshow(self._map)
        self.finished = False
        plt.ion()

    def show(self):
        self._emptyMap()
        self._markObstacle()
        self._markPerson()
        self._markExit()
        self.fig.axes.clear()
        self.fig.axes.matshow(self._map)
        plt.pause(0.5)

    def addPerson(self, person: Person):
        self.personList.append(person)

    def addExit(self, _exit: Exit):
        self.exitList.append(_exit)

    def addObstacle(self, obstacle: Obstacle):
        self.obstacleList.append(obstacle)

    def run(self):
        count = 0
        for person in self.personList:
            if person.end == 1:
                continue
            else:
                count += 1

            # 记录热力图数据
            self.hot_map[person.x, person.y] += 1

            cur_prob = 0
            cur_k = 0
            for k in range(1, 9):
                temp = self._prob_dir_(person, k)
                if temp > cur_prob:
                    cur_prob = temp
                    cur_k = k
            person.move(cur_k)
            for _exit in self.exitList:
                if person.x == _exit.x and person.y == _exit.y:
                    person.end = 1
                    break
        if count == 0:
            self.finished = True

    def _emptyMap(self):
        self._map = np.zeros(self._size)

    def _markPerson(self):
        for person in self.personList:
            self._map[person.x, person.y] = 1

    def _markExit(self):
        for _exit in self.exitList:
            self._map[_exit.x, _exit.y] = -1

    def _markObstacle(self):
        for obstacle in self.obstacleList:
            for x in range(obstacle.x1, obstacle.x2):
                for y in range(obstacle.y1, obstacle.y2):
                    self._map[x, y] = -2

    def _target_valid(self, target: tuple) -> bool:
        if target[0] < 0 or target[0] >= self._size[0]:
            return False
        if target[1] < 0 or target[1] >= self._size[1]:
            return False
        return True

    # k方向网格吸引力
    def _prob_dir_(self, person: Person, k: int) -> float:
        result = 1
        result *= self._n(person, k)
        result *= self._a_con() * self._p_con(person, k) + self._a_den() * self._p_den(person, k)
        result *= self._f_exit(person, k)
        return result

    # 网格调节系数
    def _n(self, person: Person, k: int) -> int:
        target = person.target(k)
        for obstacle in self.obstacleList:
            if obstacle.contains(target):
                return 0
        if not self._target_valid(target):
            return 0
        if self._map[target[0], target[1]] > 0:
            out = 1 - 0.05 * self._map[target[0], target[1]]
            if out < 0:
                return 0
            else:
                return out
        else:
            return 1

    # 网格吸引力概率权重因子
    @staticmethod
    def _a_con() -> float:
        return 0.85

    # 第k个方向的网格吸引力概率
    def _p_con(self, person: Person, k: int) -> float:
        return self._a_dis() * self._p_dis(person, k) \
               + self._a_dir() + self._p_dir(person, k)

    # 距离吸引力权重
    @staticmethod
    def _a_dis() -> float:
        return 0.35

    # 丛中吸引力概率
    @staticmethod
    def _a_dir() -> float:
        return 0.65

    # 距离吸引力概率
    def _p_dis(self, person: Person, k: int) -> float:
        _max = 0.0
        for _i in range(1, 9):
            if _max >= self._d_exit(person, _i):
                continue
            else:
                _max = self._d_exit(person, _i)
        return 1 - self._d_exit(person, k) / _max

    # 从众吸引力概率
    def _p_dir(self, person: Person, k: int) -> float:
        total = 0.0
        for _i in range(1, 9):
            total += self._n_dir(person, _i)
        if total == 0:
            return 0
        return self._n_dir(person, k) / total

    # 获得距离当前人最近的出口
    def _d(self, person: Person) -> Exit:
        cur_dis = 100000
        cur_exit = None
        for _exit in self.exitList:
            if _exit.getDistance(person) < cur_dis:
                cur_dis = _exit.getDistance(person)
                cur_exit = _exit
        return cur_exit

    # 第k个网格到最近出口的距离
    def _d_exit(self, person: Person, k: int) -> float:
        _exit = self._d(person)
        return _exit.getDistance(person, k)

    # 是在一定视野范围内向k方向移动的总人数
    def _n_dir(self, person: Person, k: int) -> int:
        total = 0
        for _person in self.personList:
            if person == _person:
                continue
            if _person.direction == k and person.getDistance(_person) < 2.5:
                total += 1
        return total

    # 方向k上视野范围的总人数
    def _n_field(self, person: Person, k: int) -> int:
        switch = {
            1: (0, -1),
            2: (1, -1),
            3: (1, 0),
            4: (1, 1),
            5: (0, 1),
            6: (-1, 1),
            7: (-1, 0),
            8: (-1, -1)
        }
        e1 = switch[k]
        total = 0
        for _person in self.personList:
            if person == _person:
                continue
            if _person.direction == k and person.getDistance(_person) < 5:
                e2 = (_person.x - person.x, _person.y - person.y)
                if e1[0] * e2[0] + e1[1] * e2[1] > 0:
                    total += 1
        return total

    # 方向k上的视野范围总障碍数
    def _o_field(self, person: Person, k: int) -> int:
        switch = {
            1: (0, -1),
            2: (1, -1),
            3: (1, 0),
            4: (1, 1),
            5: (0, 1),
            6: (-1, 1),
            7: (-1, 0),
            8: (-1, -1)
        }
        e1 = switch[k]
        total = 0
        for x in range(person.x - 5, person.x + 6):
            for y in range(person.y - 5, person.y + 6):
                e2 = (x - person.x, y - person.y)
                if e2[0] ** 2 + e2[1] ** 2 > 25:
                    continue
                if e1[0] * e2[0] + e1[1] * e2[1] <= 0:
                    continue
                for obstacle in self.obstacleList:
                    if obstacle.contains((x, y)):
                        total += 1
                        break
        return total

    @staticmethod
    def _a_den() -> float:
        return 0.15

    def _p_den(self, person: Person, k: int) -> float:
        n = 5
        return 1 - (self._n_field(person, k) + self._o_field(person, k)) / n ** 2

    def _f_exit(self, person: Person, k: int) -> float:
        switch = {
            1: (0, -1),
            2: (1, -1),
            3: (1, 0),
            4: (1, 1),
            5: (0, 1),
            6: (-1, 1),
            7: (-1, 0),
            8: (-1, -1)
        }
        e1 = switch[k]
        _exit = self._d(person)
        e2 = (_exit.x - person.x, _exit.y - person.y)
        res = e1[0] * e2[0] + e1[1] * e2[1]
        if res < 0:
            return 0
        else:
            return 1


if __name__ == '__main__':
    map_size = (60, 120)
    v = CA(map_size)
    v.addObstacle(Obstacle((20, 20), (25, 25)))
    v.addObstacle(Obstacle((30, 55), (40, 65)))
    v.addPerson(Person((9, 9)))
    v.addPerson(Person((9, 13)))
    v.addPerson(Person((2, 13)))
    v.addPerson(Person((4, 13)))
    v.addPerson(Person((50, 50)))
    v.addPerson(Person((4, 13)))
    v.addExit(Exit((0, 60)))
    v.addExit(Exit((30, 0)))

    for _ in range(100):
        v.show()
        v.run()
        if v.finished:
            break

    plt.matshow(v.hot_map)
    plt.pause(10)
