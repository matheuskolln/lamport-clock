from typing import List


class Event:
    def __init__(self, name: str, exec_time: int):
        self.name = name
        self.exec_time = exec_time
        self.start_time = -1


class Client:
    def __init__(self, id: int):
        self.events: List[Event] = []
        self.id = id

    def add_event(self, name, exec_time):
        event = Event(name, exec_time)
        self.events.append(event)

    def get_events(self):
        return self.events

    def get_total_time(self):
        total_time = 0
        for event in self.events:
            total_time += event.exec_time
        return total_time

    def get_lamport_times(self):
        return sorted([event.start_time for event in self.events])
