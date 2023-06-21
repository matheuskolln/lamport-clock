import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from client import Client
from server import Server


def plot_gantt_chart(clients):
    """
    Generates a chart visualizing the timeline of events for each client.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.get_cmap("tab10").colors
    y_ticks = []
    y_labels = []

    for i, client in enumerate(clients):
        event_count = len(client.get_events())
        event_names = [event.name for event in client.get_events()]
        event_exec_times = [event.exec_time for event in client.get_events()]
        start_times = [event.start_time for event in client.get_events()]

        y_ticks.append(i)
        y_labels.append(f"Client {client.id}")

        for j in range(event_count):
            ax.broken_barh(
                [(start_times[j], event_exec_times[j])],
                (i - 0.4, 0.8),
                facecolors=colors[j % len(colors)],
            )
            ax.text(
                start_times[j] + event_exec_times[j] / 2,
                i,
                event_names[j],
                ha="center",
                va="center",
            )

    ax.set_xlabel("Time")
    ax.set_ylabel("Client")
    ax.set_title("Timeline of Events")
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xticks(
        range(
            0,
            max(
                [
                    event.start_time + event.exec_time
                    for client in clients
                    for event in client.get_events()
                ]
            )
            + 1,
            1,
        )
    )
    ax.grid(True)
    plt.savefig("chart.png")  # Save the chart as an image file
    plt.close()


def create_client_window(clients, menu_frame):
    def add_event():
        event_name = event_name_entry.get()
        exec_time = int(exec_time_entry.get())
        client.add_event(event_name, exec_time)
        event_name_entry.delete(0, tk.END)
        exec_time_entry.delete(0, tk.END)
        event_name_entry.focus_set()
        events_listbox.insert(tk.END, f"{event_name} (Execution Time: {exec_time}s)")

    def finish():
        if len(client.get_events()) == 0:
            tk.messagebox.showwarning("No Events", "Please add at least one event.")
        else:
            clients.append(client)
            refresh_clients()
            root.destroy()

    client = Client(len(clients) + 1)
    root = tk.Toplevel()
    root.title("Create Client")
    root.geometry("400x500")

    event_frame = ttk.Frame(root)

    event_name_label = ttk.Label(event_frame, text="Event Name:", font=("Arial", 12))
    event_name_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    event_name_entry = ttk.Entry(event_frame, font=("Arial", 12))
    event_name_entry.grid(row=0, column=1, pady=10, padx=10)
    event_name_entry.focus_set()

    exec_time_label = ttk.Label(event_frame, text="Execution Time:", font=("Arial", 12))
    exec_time_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
    exec_time_entry = ttk.Entry(event_frame, font=("Arial", 12))
    exec_time_entry.grid(row=1, column=1, pady=10, padx=10)

    add_button = ttk.Button(
        event_frame,
        text="Add Event",
        command=add_event,
        style="AccentButton.TButton",
    )
    add_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    events_frame = ttk.Frame(root)
    events_frame.pack(fill="both", expand=True, padx=10, pady=10)

    events_label = ttk.Label(
        events_frame, text="Events:", font=("Arial", 12), anchor="w"
    )
    events_label.pack(fill="x", pady=10)

    events_listbox = tk.Listbox(events_frame, width=40, height=8, font=("Arial", 12))
    events_listbox.pack(fill="both", expand=True, padx=10)

    event_scrollbar = ttk.Scrollbar(
        events_frame, orient=tk.VERTICAL, command=events_listbox.yview
    )
    events_listbox.configure(yscrollcommand=event_scrollbar.set)
    event_scrollbar.pack(side=tk.RIGHT, fill="y")

    event_frame.pack(padx=10, pady=10)

    finish_button = ttk.Button(
        root,
        text="Finish",
        command=finish,
        style="AccentButton.TButton",
    )
    finish_button.pack(pady=10)

    def refresh_clients():
        menu_frame.configure(state="normal")
        menu_frame.delete("1.0", tk.END)
        menu_frame.insert(tk.END, "Clients:\n\n")
        for i, c in enumerate(clients, start=1):
            menu_frame.insert(tk.END, f"Client {i}\n")
            for event in c.get_events():
                menu_frame.insert(
                    tk.END, f"- {event.name} (Execution Time: {event.exec_time}s)\n"
                )
            menu_frame.insert(tk.END, "\n")
        menu_frame.configure(state="disabled")


def execute_events(clients):
    print("\nExecuting events randomly...")
    all_events = [client.get_events() for client in clients]
    flat_events = [event for client_events in all_events for event in client_events]
    random.shuffle(flat_events)

    server = Server()
    for event in flat_events:
        client_id = random.randint(1, len(clients))
        server.process_event(event, client_id)

    print("\nAll events executed!")
    plot_gantt_chart(clients)


def main():
    clients = []
    root = tk.Tk()
    root.title("Menu")
    root.geometry("400x500")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    menu_frame = tk.Text(main_frame, width=40, height=10, font=("Arial", 12))
    menu_frame.pack(fill=tk.BOTH, padx=10, pady=10)
    menu_frame.configure(state="disabled")

    def refresh_clients():
        menu_frame.configure(state="normal")
        menu_frame.delete("1.0", tk.END)
        menu_frame.insert(tk.END, "Clients:\n\n")
        for i, c in enumerate(clients, start=1):
            menu_frame.insert(tk.END, f"Client {i}\n")
            for event in c.get_events():
                menu_frame.insert(
                    tk.END, f"- {event.name} (Execution Time: {event.exec_time}s)\n"
                )
            menu_frame.insert(tk.END, "\n")
        menu_frame.configure(state="disabled")

    refresh_clients()

    create_button = ttk.Button(
        main_frame,
        text="Create a Client",
        command=lambda: create_client_window(clients, menu_frame),
        style="AccentButton.TButton",
    )
    create_button.pack(pady=10)

    execute_button = ttk.Button(
        main_frame,
        text="Execute Events",
        command=lambda: execute_events(clients),
        style="AccentButton.TButton",
    )
    execute_button.pack(pady=10)

    exit_button = ttk.Button(
        main_frame,
        text="Exit",
        command=root.destroy,
        style="AccentButton.TButton",
    )
    exit_button.pack(pady=10)

    style = ttk.Style()
    style.configure("AccentButton.TButton", font=("Arial", 12))

    root.mainloop()


if __name__ == "__main__":
    main()
