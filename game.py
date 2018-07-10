# -*- coding: utf-8 -*-
import numpy as np
# from numpy.random import randint

import random
import sys
import time
# random.choiceでコケた
# 再帰に上限値があるの初めて知った
sys.setrecursionlimit(1000000000)


class Game(object):
    """
    LifeGame

    limit
    * not for
    * not if
    * not 4 line over method
    """

    def __init__(self, field_length, field=[]):
        self.field_length = field_length
        self.cell_length = field_length ** 2
        # self.field = randint(0, 2, self.cell_length)
        self.field = [0] * self.cell_length
        self.field = self.format_field([self.field, field][len(field) != 0])

    def format_field(self, field):
        """
        random valueによる初期値設定
        from numpy.random import randint
        で簡単にできるl
        :return: 
        """
        print(self.field, field)
        functions = [self.loop_list,
                     lambda x, _: x]
        return functions[sum(field) != 0](field, self.set_random)

    @staticmethod
    def set_random(*_):
        """
        ランダムに, 0, 1を返す
        引数なしにしたかった
        """
        return random.choice([0, 1])

    def run(self):
        self.loop_list(self.field, self.show_cell)
        self.field = self.loop_list(list(self.field), self.is_alive)
        print('-' * self.field_length * 2)
        time.sleep(0.5)
        self.run()

    def loop_list(self, list_, func, count=0):
        functions = [self.exit_loop, self.loop_list]
        list_[count] = func(list_, count)
        count += 1
        return functions[count < len(list_)](list_, func, count)

    @staticmethod
    def exit_loop(list_, *_):
        return list_

    def show_cell(self, list_, index):
        end = ['\n', '']
        show_value = ['□', '◼'][list_[index]]
        print(f'{show_value} ', end=end[(index + 1) % self.field_length != 0])
        return list_[index]

    @staticmethod
    def is_alive_from_alive(value):
        return int(value in [2, 3])

    @staticmethod
    def is_alive_from_dead(value):
        return int(value in [3])

    def is_alive(self, list_, index):
        functions = [self.is_alive_from_dead, self.is_alive_from_alive]
        sum_around = sum(self.around(index))
        return functions[list_[index]](sum_around)

    def get_around_indexs(self, index):
        cells = [index - self.field_length, index + self.field_length]
        cells += [[], [index - self.field_length - 1, index - 1, index + self.field_length - 1]][index % self.field_length != 0]
        cells += [[], [index - self.field_length + 1, index + 1, index + self.field_length + 1]][(index + 1) % self.field_length != 0]
        return cells

    def around(self, index):
        indexs = self.get_around_indexs(index)
        # print(index, self.field)
        # print(index, indexs)
        values = self.loop_list(indexs, self.get_cell)
        # print(index, values)
        return values

    def get_cell(self, list_, count):
        index = list_[count]
        run_flg = 0 <= index < self.cell_length
        get_func = [self.get_none, self.get_value][run_flg]
        return get_func(index)

    @staticmethod
    def get_none(_):
        return 0

    def get_value(self, index):
        return self.field[index]


if __name__ == '__main__':
    game = Game(32)
    game.run()
