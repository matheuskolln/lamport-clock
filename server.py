from client import Event
from lamport import LamportClock


class Server:
    def __init__(self):
        self.clock = LamportClock()

    def process_event(self, event: Event, client_id: int):
        start_time = self.clock.clock
        print(
            f"Processing event '{event.name}' for Client {client_id} at Lamport time {start_time}. Exec time = {event.exec_time}s"
        )
        event.start_time = start_time
        self.clock.update(start_time + event.exec_time)
        print(
            f"Event '{event.name}' processed for Client {client_id} at Lamport time {self.clock.clock}"
        )
