import threading


class Server:
    def __init__(self, clock):
        """
        Server class represents a server that processes requests from clients.

        Args:
            clock (LamportClock): Lamport clock instance for tracking time.
        """
        self.clock = clock
        self.processes = []
        self.processes_lock = threading.Lock()
        self.mutex = threading.Lock()
        self.agreement = threading.Condition(self.mutex)

    def add_process(self, process_id, execution_time):
        """
        Adds a new process to the server's queue of processes.

        Args:
            process_id (int): ID of the process.
            execution_time (int): Execution time of the process.
        """
        with self.processes_lock:
            # Add the process with its Lamport time, process ID, and execution time
            self.processes.append((self.clock.clock, process_id, execution_time))
            # Sort the processes based on their execution time
            self.processes.sort(key=lambda x: x[2])

    def process_request(self, client_id, info_lock, info_label_var):
        """
        Processes a request from a client and updates the Lamport clock.

        Args:
            client_id (int): ID of the client sending the request.
            info_lock (threading.Lock): Lock for thread-safe access to the info_label_var.
            info_label_var (tkinter.StringVar): Variable for displaying information in the GUI.

        Returns:
            int: Updated Lamport time after processing the request.
        """
        start_time = self.clock.clock
        execution_time = self.processes[client_id - 1][2]

        with self.mutex:
            with info_lock:
                info_label_var.set(
                    info_label_var.get()
                    + f"\nServer: Processing request from Client {client_id} at Lamport time {start_time}"
                )
            print(
                f"Server: Processing request from Client {client_id} at Lamport time {start_time}"
            )
            updated_time = self.clock.update(start_time + execution_time)

            self.agreement.notify_all()
        return updated_time
