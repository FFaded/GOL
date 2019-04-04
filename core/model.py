import copy
import random
import time


class Model:
    def __init__(self, width=150, length=150, frequency=4, cycle_length=0.03):
        self._width = width
        self._length = length
        self._frequency = frequency
        self._cycle_length = cycle_length
        self._playing = False
        self.game_area = [[False for _ in range(length)] for _ in range(width)]
        self.living_game_area = [[False for _ in range(length)] for _ in range(width)]
        self.init_game_area()

    def stop(self):
        self._playing = False

    def evolve(self):
        for i in range(self._width):
            for j in range(self._length):
                self._cell_lives(i, j)

        self.game_area = copy.deepcopy(self.living_game_area)
        time.sleep(self._cycle_length)

    def clear(self):
        self.game_area = [[False for _ in range(self._length)] for _ in range(self._width)]

    def get_dimensions(self):
        return self._width, self._length

    def is_playing(self):
        return self._playing

    def speed_up(self):
        self._cycle_length /= 2

    def speed_down(self):
        self._cycle_length += 0.05

    def init_game_area(self):
        for i in range(self._width):
            for j in range(self._length):
                self.game_area[i][j] = random.randint(0, self._frequency) % (self._frequency + 1) == 0

    def _cell_lives(self, i, j):
        adjacent_cells_count = self._adjacent_alive_cells_count(i, j)
        self.living_game_area[i][j] = adjacent_cells_count == 3 or (adjacent_cells_count == 2 and self.game_area[i][j])

    def _adjacent_alive_cells_count(self, i, j):
        count = 0
        if i > 0:
            count += int(self.game_area[i - 1][j])
            if j > 0:
                count += int(self.game_area[i - 1][j - 1])
            if j < self._length - 1:
                count += int(self.game_area[i - 1][j + 1])

        if i < self._width - 1:
            count += int(self.game_area[i + 1][j])
            if j > 0:
                count += int(self.game_area[i + 1][j - 1])
            if j < self._length - 1:
                count += int(self.game_area[i + 1][j + 1])

        if j > 0:
            count += int(self.game_area[i][j - 1])

        if j < self._length - 1:
            count += int(self.game_area[i][j + 1])

        return count
