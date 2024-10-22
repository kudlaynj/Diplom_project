from datetime import datetime
from time import sleep
from threading import Thread

time_start = datetime.now()


class Train(Thread):
    def __init__(self, train):
        super().__init__()
        self.train = train
        self.speed = 100
        self.hour = 1
        self.numb_station = 100

    def way_start(self):
        print(f'{self.train}, отправляется')

    def way_end(self):
        print(f'Поезд {self.train} прибыл на конечную станцию спустя {self.hour-1} часов(часа)!')

    def run(self):
        self.way_start()
        while self.numb_station > 0 and self.hour <= 10:
            print(f'Поезд {self.train}, в пути {self.hour} часов(часа), осталось {self.numb_station} станций.')
            self.speed -= 10
            self.numb_station -= 10
            self.hour += 1
            sleep(1)
        self.way_end()


train_path_1 = Train("Москва - Ижевск")
train_path_2 = Train("Москва - Владивосток")

train_path_1.start()
train_path_2.start()

train_path_1.join()
train_path_2.join()

time_end = datetime.now()
time_res = time_end - time_start

print(f"Время пути: {time_res}")
