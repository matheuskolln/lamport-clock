import time


class Client:
    def __init__(self, client_id, server, info_lock, info_label_var):
        """
        Client class represents a client process that sends requests to the server.

        Args:
            client_id (int): ID of the client.
            server (Server): Server instance to send requests to.
            info_lock (threading.Lock): Lock for thread-safe access to the info_label_var.
            info_label_var (tkinter.StringVar): Variable for displaying information in the GUI.
        """
        self.client_id = client_id
        self.server = server
        self.lamport_times = []
        self.info_lock = info_lock
        self.info_label_var = info_label_var

    def send_request(self, execution_time):
        """
        Sends a request to the server and processes the response.

        Args:
            execution_time (int): Time to simulate the processing of the request.

        """
        received_time = self.server.process_request(
            self.client_id, self.info_lock, self.info_label_var
        )
        self.lamport_times.append(received_time)
        with self.info_lock:
            self.info_label_var.set(
                self.info_label_var.get()
                + f"\nClient {self.client_id}: Request processed at Lamport time {received_time} (Execution Time: {execution_time}s)"
            )
        print(
            f"Client {self.client_id}: Request processed at Lamport time {received_time} (Execution Time: {execution_time}s)"
        )
        time.sleep(execution_time)
