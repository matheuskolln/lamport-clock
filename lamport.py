"""
The Lamport clock is an algorithm used to order concurrent
events in distributed systems. It assigns a timestamp to
each event, allowing you to determine the order in which
they occurred.
"""


import os
import tkinter as tk
import matplotlib.pyplot as plt  # type: ignore
from PIL import Image, ImageTk  # type: ignore
import random  # type: ignore


def print_event_logs(event_logs):
    for process_id, event_log in event_logs.items():
        timestamps = list(dict.fromkeys([str(timestamp) for timestamp, _ in event_log]))

        print(f"P{process_id}: {', '.join(timestamps)}")


def get_event_logs_strings(event_logs):
    strings = []
    for process_id, event_log in event_logs.items():
        timestamps = list(dict.fromkeys([str(timestamp) for timestamp, _ in event_log]))
        strings.append(f"P{process_id}: {', '.join(timestamps)}")
    return strings


def clear_console():
    for _ in range(0, 20):
        print("\n")


class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

    def get_time(self):
        return self.time


class LamportProcess:
    def __init__(self, process_id, lamport_clock):
        self.process_id = process_id
        self.clock = lamport_clock

    def send_message(self, dest_process_id, message):
        self.clock.tick()
        # Simulate sending the message
        # Increment Lamport clock before sending
        # Send the message to the destination process

    def receive_message(self, source_process_id, message):
        self.clock.update(message["timestamp"])
        # Simulate receiving the message
        # Update Lamport clock based on the received timestamp

    def run_event(self):
        self.clock.tick()
        # Simulate running a local event
        # Perform some local action

    def process_event(self, event):
        event_type = event["type"]
        if event_type == "send":
            dest_process_id = event["dest_process_id"]
            message = event["message"]
            self.send_message(dest_process_id, message)
        elif event_type == "receive":
            source_process_id = event["source_process_id"]
            message = event["message"]
            self.receive_message(source_process_id, message)
        elif event_type == "local":
            self.run_event()


class LamportSimulationApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Lamport Clock Simulation")
        self.process_labels = []
        self.chart_label = None
        self.events = []

        self.create_process_button = tk.Button(
            self.window,
            text="Create Process",
            command=self.create_process,
            font=("Arial", 16),
        )
        self.create_process_button.place(x=10, y=10)

        self.run_button = tk.Button(
            self.window,
            text="Run Simulation",
            command=self.run_simulation,
            font=("Arial", 16),
        )
        self.run_button.place(x=326, y=10)

        self.reset_button = tk.Button(
            self.window,
            text="Reset Simulation",
            command=self.reset_simulation,
            font=("Arial", 16),
            state=tk.DISABLED,
        )
        self.reset_button.place(x=612, y=10)

        self.chart_label = tk.Label(self.window)
        self.chart_label.place(x=10, y=150)

        self.window.geometry("800x600")
        self.window.resizable(width=False, height=False)

    def generate_random_events(self, num_processes):
        events = [[] for _ in range(num_processes)]
        for process_id in range(num_processes):
            # Determine the number of events for the current process
            num_process_events = random.randint(1, 7)

            # Generate sequential timestamps for the events within the process
            timestamps = list(range(1, num_process_events + 1))

            # Generate events for the current process
            receivers = set(range(num_processes))
            receivers.remove(process_id)  # Exclude self from receivers

            for i, timestamp in enumerate(timestamps):
                event_type = random.choice(["local", "send"])

                if event_type == "send":
                    dest_process_id = random.choice(list(receivers))

                    event = {
                        "type": "send",
                        "timestamp": timestamp,
                        "dest_process_id": dest_process_id,
                        "message": {"timestamp": timestamp},
                    }
                    events[process_id].append(event)

                    receiver_event = {
                        "type": "receive",
                        "timestamp": timestamp + 1,
                        "source_process_id": process_id,
                        "message": {"timestamp": timestamp + 1},
                    }

                    events[dest_process_id].append(receiver_event)

                else:
                    # Generate local event
                    event = {"type": "local", "timestamp": timestamp}
                    events[process_id].append(event)

        return events

    def lamport_simulation(self, events):
        lamport_clock = LamportClock()
        processes = {}
        event_logs = {}  # Stores events and timestamps

        # Create the processes
        for process_id in range(len(events)):
            process = LamportProcess(process_id, lamport_clock)
            processes[process_id] = process

        # Insert events into the event logs
        for process_id, event_list in enumerate(events):
            if process_id not in event_logs:
                event_logs[process_id] = []
            for event in event_list:
                if "timestamp" in event:
                    timestamp = event["timestamp"]
                    event_logs[process_id].append((timestamp, event))

        # Sort the events within each process based on timestamp
        for process_id, event_log in event_logs.items():
            event_logs[process_id] = sorted(event_log, key=lambda x: (x[0], process_id))

        # Process the events in order
        for timestamp in range(1, len(events) * 3 + 1):
            for process_id in range(len(events)):
                for event_timestamp, event in event_logs[process_id]:
                    if event_timestamp == timestamp:
                        process = processes[process_id]
                        process.process_event(event)

        return event_logs

    def start(self):
        self.window.mainloop()

    def create_process(self):
        if len(self.process_labels) < 10:
            # Create the process label
            label_text = f"Process {len(self.process_labels)}"
            label = tk.Label(self.window, text=label_text, font=("Arial", 16))
            self.process_labels.append(label)
            label.place(x=660, y=30 + len(self.process_labels) * 22)
            self.enable_buttons()

    def run_simulation(self):
        if len(self.process_labels) > 0:
            # Generate random events for all processes
            random_events = self.generate_random_events(len(self.process_labels))

            # Create the LamportClock and LamportProcess objects for each process
            lamport_clocks = [LamportClock() for _ in range(len(self.process_labels))]
            processes = [
                LamportProcess(i + 1, clock) for i, clock in enumerate(lamport_clocks)
            ]
            self.events = random_events
            # Run the simulation with the generated events
            event_logs = self.lamport_simulation(random_events)

            # Print the final clock of each process
            for process_id, _ in enumerate(processes):
                print(
                    f"Process {process_id} Final Clock - {event_logs[process_id][-1][1]['timestamp']}"
                )

            # Print the event logs
            print_event_logs(event_logs)
            self.reset_button.configure(state=tk.NORMAL)
            self.run_button.configure(state=tk.DISABLED)
            self.create_process_button.configure(state=tk.DISABLED)

            self.show_chart()
            timestamps = get_event_logs_strings(event_logs)
            for x, timestamp in enumerate(timestamps):
                label = tk.Label(self.window, text=timestamp, font=("Arial", 12))
                self.process_labels.append(label)
                label.place(x=650, y=50 + (len(self.process_labels) * 22) + x * 5)

            return event_logs

    def show_chart(self):
        if self.chart_label is not None:
            self.chart_label.destroy()

        # Generate and plot the chart
        fig, ax = plt.subplots()

        # Plot horizontal lines for each process
        for process_id in range(len(self.events)):
            plt.axhline(y=process_id, color="gray", linestyle="--")
        event_logs = self.lamport_simulation(self.events)
        # Plot events with dots and labels
        for process_id, event_log in event_logs.items():
            for timestamp, event in event_log:

                plt.annotate(
                    timestamp,
                    (timestamp, process_id),
                    xytext=(5, -10),
                    textcoords="offset points",
                )

                plt.plot(timestamp, process_id, "o", markersize=10)

        # Plot message arrows as lines between senders and receivers
        for process_id, event_log in event_logs.items():
            for timestamp, event in event_log:
                if event["type"] in ["send"]:
                    dest_process_id = (
                        event["dest_process_id"]
                        if "dest_process_id" in event
                        else event["source_process_id"]
                    )
                    sender_coords = (timestamp, process_id)
                    receiver_coords = (timestamp + 1, dest_process_id)
                    plt.arrow(
                        sender_coords[0],
                        sender_coords[1],
                        receiver_coords[0] - sender_coords[0],
                        receiver_coords[1] - sender_coords[1],
                        color="black",
                        head_width=0.1,
                        head_length=0.2,
                        length_includes_head=True,
                        linewidth=1.5,
                        linestyle="-",
                    )

        # Adjust y-axis limits
        plt.ylim([-1, len(self.process_labels) + 1])

        # Extract all timestamps from event logs
        timestamps = [
            timestamp for event_log in event_logs.values() for timestamp, _ in event_log
        ]

        # Adjust x-axis limits
        min_timestamp = 0
        max_timestamp = max(timestamps) if timestamps else 1
        plt.xlim([min_timestamp, max_timestamp + 1])

        plt.xlabel("Timestamp")
        plt.ylabel("Process ID")
        plt.title("Lamport Clock - Event Timeline")
        plt.yticks(list(event_logs.keys()))  # Set y-axis labels to process IDs
        plt.ylim([-1, len(self.process_labels)])  # Adjust y-axis limits
        plt.savefig("chart.png")

        if os.path.exists("chart.png"):
            # Load the image
            chart_image = Image.open("chart.png")

            # Resize the chart image to fit the label
            width, height = chart_image.size
            if width > 700 or height > 500:
                ratio = min(700 / width, 500 / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                chart_image = chart_image.resize(
                    (new_width, new_height), Image.ANTIALIAS
                )

            # Convert the PIL image to a Tkinter image
            tk_image = ImageTk.PhotoImage(chart_image)

            # Update the chart label with the new image
            self.chart_label = tk.Label(self.window, image=tk_image)
            self.chart_label.image = (
                tk_image  # Store a reference to avoid garbage collection
            )
            self.chart_label.place(x=10, y=75)

    def reset_simulation(self):
        clear_console()
        print(f"Simulation has been reset.")
        # Destroy the process labels
        for label in self.process_labels:
            label.destroy()
        self.process_labels.clear()

        # Destroy the chart label and disable the reset button
        self.chart_label.configure(image="")
        self.reset_button.configure(state=tk.DISABLED)
        self.run_button.configure(state=tk.NORMAL)
        self.create_process_button.configure(state=tk.NORMAL)

    def enable_buttons(self):
        self.reset_button.configure(state=tk.NORMAL)
        self.run_button.configure(state=tk.NORMAL)


def main():
    app = LamportSimulationApp()
    app.start()


if __name__ == "__main__":
    main()
