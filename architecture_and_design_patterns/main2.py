import random

class Print:

    count = 10

    def __init__(self, name):
        self.name = name

    def pp(self):
        print(self.name)


    def print_count(self):
        print(self.count)

    def pp_plus(self):
        self.name += 'koya'


p = Print('vasya')
# p.pp_plus()
# p.pp()
# print(random.random())
p.print_count()