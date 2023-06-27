"""
A mobile sequencer in distributed systems is a component responsible for
coordinating and executing operations on distributed mobile devices.
It manages the execution order of operations received from different devices,
ensuring data consistency and integrity during processing. This approach allows
mobile devices to send operations for centralized processing and receive the results back.
The mobile sequencer ensures that operations are executed in the correct order, regardless
of origin or submission time, preventing conflicts in distributed environments.
"""


import random
import threading
import time
import queue


class Operation:
    def __init__(self, description):
        self.id = None
        self.description = description

    def execute(self):
        print(f"Starting operation {self.id}: {self.description}")
        processing_time = random.uniform(1.2, 2.5)
        time.sleep(processing_time)  # Simulate operation processing time
        print(f"Operation {self.id} completed ({processing_time:.2f}s)")


class MobileSequencer:
    def __init__(self):
        self.lock = threading.Lock()
        self.sequence_number = 0
        self.pending_operations = queue.Queue()
        self.executed_operations = []
        self.num_threads = 3

    def add_operation(self, operation):
        with self.lock:
            operation.id = self.sequence_number
            self.sequence_number += 1
        self.pending_operations.put(operation)

    def process_operations(self):
        def process():
            while True:
                if not self.pending_operations.empty():
                    operation = self.pending_operations.get()
                    operation.execute()
                    self.executed_operations.append(operation)
                else:
                    time.sleep(1)  # Wait for new operations

        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=process)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def get_executed_operations(self):
        return self.executed_operations


sequencer = MobileSequencer()

# Simulate adding operations
operations = [Operation(f"Operation {i}") for i in range(0, 10)]

# Add operations to the sequencer
for operation in operations:
    sequencer.add_operation(operation)

# Start processing operations in multiple threads
processing_thread = threading.Thread(target=sequencer.process_operations)
processing_thread.start()

# Simulate other activities running in parallel
def simulate_other_activities():
    for i in range(6):
        print(f"Performing other activity {i}")
        time.sleep(1)


other_activities_thread = threading.Thread(target=simulate_other_activities)
other_activities_thread.start()

other_activities_thread.join()
processing_thread.join()
