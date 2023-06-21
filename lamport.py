class LamportClock:
    def __init__(self):
        self.clock = 0

    def increment(self) -> int:
        self.clock += 1
        return self.clock

    def update(self, received_time: int) -> int:
        self.clock = max(self.clock, received_time)
        return self.clock
