import threading
import time
import tkinter as tk
import random
from typing import List
from chart import generate_chart
from lamport import LamportClock
from server import Server
from client import Client
from PIL import ImageTk, Image


def add_process():
    """
    Adds a new process to the server's process list with a randomly generated execution time.
    Updates the GUI to display the added process.
    """
    if len(server.processes) < 10:
        process_id = len(server.processes) + 1
        execution_time = random.randint(1, 3)
        server.add_process(process_id, execution_time)
        process_label = tk.Label(
            frame,
            text=f"Process {process_id} (Time: {execution_time}s)",
            font="Helvetica 12 bold",
        )
        process_label.pack()


def run_clock():
    """
    Starts the clock by running the client processes.
    Disables relevant GUI buttons during clock execution.
    """
    global clock_running
    clock_running = True
    with info_lock:
        info_label_var.set("Running Lamport Clock...")
    run_button.config(state=tk.DISABLED)
    add_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)

    def run_clients():
        """
        Starts the client processes for each process in the server's process list.
        Updates the chart dynamically after each process finishes execution.
        """
        total_execution_time = sum([process[2] for process in server.processes])
        for i, (_, process_id, execution_time) in enumerate(server.processes):
            client = Client(process_id, server, info_lock, info_label_var)
            clients.append(client)

            total_execution_time -= execution_time

            threading.Thread(target=client.send_request, args=(execution_time,)).start()

            # Introduce delay before starting the next client process
            time.sleep(execution_time)

            root.after(
                0, update_chart
            )  # Generate and display the chart after each process finishes

    update_chart()  # Generate and display the initial empty chart

    threading.Thread(target=run_clients).start()

    reset_button.config(state=tk.NORMAL)


def update_chart():
    """
    Generates and displays the chart dynamically.
    """
    with chart_lock:
        processes = [
            (process[1], process[0], process[2]) for process in server.processes
        ]
        generate_chart(clients, processes)

        updated_chart_image = ImageTk.PhotoImage(Image.open("chart.png"))
        chart_label.configure(image=updated_chart_image)
        chart_label.image = updated_chart_image


def reset(clock: LamportClock):
    """
    Resets the clock, server's process list, and clears the GUI labels.
    Enables relevant GUI buttons after reset.
    """
    global clock_running
    clock_running = False
    server.processes = []
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label) and "Process" in widget["text"]:
            widget.destroy()
    with info_lock:
        info_label_var.set("Lamport Clock Reset.")
    run_button.config(state=tk.NORMAL)
    add_button.config(state=tk.NORMAL)
    reset_button.config(state=tk.NORMAL)
    clock.reset()
    clients.clear()
    update_chart()


if __name__ == "__main__":
    clock = LamportClock()
    server = Server(clock)
    clients: List[Client] = []

    root = tk.Tk()
    root.title("Lamport Clock")

    info_lock = threading.Lock()
    info_label_var = tk.StringVar()
    chart_lock = threading.Lock()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    add_button = tk.Button(
        frame, text="Add Process", command=add_process, font="Helvetica 12 bold"
    )
    add_button.pack(side=tk.LEFT, padx=10)

    run_button = tk.Button(
        frame, text="Run Clock", command=run_clock, font="Helvetica 12 bold"
    )
    run_button.pack(side=tk.LEFT, padx=10)

    reset_button = tk.Button(
        frame, text="Reset", command=lambda: reset(clock), font="Helvetica 12 bold"
    )
    reset_button.pack(side=tk.LEFT, padx=10)

    info_label = tk.Label(
        root, textvariable=info_label_var, font="Helvetica 14 bold", pady=10
    )
    info_label.pack()

    chart_frame = tk.Frame(root)
    chart_frame.pack()
    chart_image = ImageTk.PhotoImage(Image.open("chart.png"))

    chart_label = tk.Label(chart_frame, image=chart_image)
    chart_label.pack()

    clock_running = False

    root.after(0, update_chart)

    root.mainloop()
