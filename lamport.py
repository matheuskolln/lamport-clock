import threading


class LamportClock:
    def __init__(self):
        """
        LamportClock class represents a Lamport logical clock for tracking time.

        """
        self.clock = 0
        self.lock = threading.Lock()

    def increment(self) -> int:
        """
        Increments the Lamport clock by one unit and returns the updated value.

        Returns:
            int: Updated Lamport time after incrementing.
        """
        with self.lock:
            self.clock += 1
            return self.clock

    def update(self, received_time: int) -> int:
        """
        Updates the Lamport clock based on the received time and returns the updated value.

        Args:
            received_time (int): The received time to update the Lamport clock.

        Returns:
            int: Updated Lamport time after updating with the received time.
        """
        with self.lock:
            self.clock = max(self.clock, received_time)
            return self.clock

    def reset(self):
        """
        Resets the Lamport clock to the initial value (0).
        """
        self.clock = 0
