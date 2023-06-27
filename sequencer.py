"""
A mobile sequencer in distributed systems is a component responsible for
coordinating and executing operations on distributed mobile devices.
It manages the execution order of operations received from different devices,
ensuring data consistency and integrity during processing. This approach allows
mobile devices to send operations for centralized processing and receive the results back.
The mobile sequencer ensures that operations are executed in the correct order, regardless
of origin or submission time, preventing conflicts in distributed environments.
"""


import threading
import time
import queue


class Operation:
    def __init__(self, description):
        self.id = None
        self.description = description

    def execute(self):
        print(f"Starting operation {self.id}: {self.description}")
        time.sleep(1)  # Simulate operation processing time
        print(f"Operation {self.id} completed")


class MobileSequencer:
    def __init__(self):
        self.lock = threading.Lock()
        self.sequence_number = 0
        self.pending_operations = queue.Queue()
        self.executed_operations = []

    def add_operation(self, operation):
        with self.lock:
            operation.id = self.sequence_number
            self.sequence_number += 1
        self.pending_operations.put(operation)

    def process_operations(self):
        while True:
            if not self.pending_operations.empty():
                operation = self.pending_operations.get()
                operation.execute()
                self.executed_operations.append(operation)
            else:
                time.sleep(1)  # Wait for new operations

    def get_executed_operations(self):
        return self.executed_operations


sequencer = MobileSequencer()

# Simulate adding operations
operations = [Operation(f"Operation {i}") for i in range(1, 11)]

# Add operations to the sequencer
for operation in operations:
    sequencer.add_operation(operation)

# Start processing operations in a separate thread
processing_thread = threading.Thread(target=sequencer.process_operations)
processing_thread.start()

# Simulate other activities running in parallel
for i in range(len(operations)):
    print(f"Performing other activity {i}")
    time.sleep(1)

# Wait for all operations to complete
processing_thread.join()

# Get the executed operations from the sequencer
executed_operations = sequencer.get_executed_operations()
print("Executed Operations:")
for operation in executed_operations:
    print(f"ID: {operation.id}, Description: {operation.description}")
