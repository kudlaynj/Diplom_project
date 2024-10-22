from multiprocessing import Queue, Lock

"""Исполнения многопроцессного программирования, 
   на пирмере оброботки пассажиропотока на автобусном маршруте"""


class WarehouseManager:
    def __init__(self, entrance, exit):
        self.data = {}
        self.entrance = entrance
        self.exit = exit
        self.queue = Queue()
        self.lock = Lock()
        self.requests = [
            ("bus_stop1", "entrance", 34),
            ("bus_stop2", "entrance", 46),
            ("bus_stop1", "exit", 17),
            ("bus_stop3", "entrance", 31),
            ("bus_stop2", "exit", 37)
        ]

    def process_request(self):
        for product, action, amount in self.requests:
            with self.lock:
                if product not in self.data:
                    self.data[product] = 0
                if action == "entrance":
                    self.data[product] += amount
                elif action == "exit":
                    self.data[product] = max(0, self.data[product] - amount)

    def run(self):
        self.process_request()


if __name__ == '__main__':
    manager = WarehouseManager(13, 21)
    manager.run()
    print(manager.data)
