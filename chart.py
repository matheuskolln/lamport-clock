from typing import List, Tuple
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt

from client import Client


COMMON_COLORS = [
    "blue",
    "red",
    "orange",
    "yellow",
    "green",
    "purple",
    "pink",
    "brown",
    "gray",
    "cyan",
]


def generate_chart(clients: List[Client], processes: Tuple[int, int, int]):
    """
    Generates a chart visualizing the Lamport clock and client processes.
    """
    plt.figure(figsize=(10, 6))
    total_time = sum([process[2] for process in processes])  # type: ignore

    if not clients:
        # No processes to display, show an empty chart with appropriate labels
        plt.xlabel("Lamport Time")
        plt.ylabel("Process")
        plt.title("Lamport Clock (No Processes)")
        plt.grid(True)
        plt.savefig("chart.png")  # Save the chart as an image file
        plt.close()
        return

    for i, client in enumerate(clients):
        process_id = client.client_id
        lamport_times = client.lamport_times
        color = COMMON_COLORS[i % len(COMMON_COLORS)]
        plt.plot(
            lamport_times,
            [process_id] * len(lamport_times),
            marker="o",
            markersize=14,
            color=color,
            label=f"Process {process_id}",
        )
        for j, time in enumerate(lamport_times):
            plt.text(
                time + (0.01 * total_time),
                process_id,
                str(process_id),
                horizontalalignment="left",
                verticalalignment="bottom",
                size=12,
            )

    for client in clients:
        lamport_times = client.lamport_times
        process_id = client.client_id
        for i in range(len(lamport_times) - 1):
            plt.plot(
                [lamport_times[i], lamport_times[i + 1]],
                [process_id, process_id],
                color="black",
                linestyle="dashed",
                linewidth=0.5,
            )
    plt.xlabel("Lamport Time")
    plt.ylabel("Process")
    plt.title("Lamport Clock")
    plt.yticks(range(1, len(processes) + 1))
    plt.xticks(range(0, total_time + 1, 1))
    plt.legend()
    plt.grid(True)
    plt.savefig("chart.png")  # Save the chart as an image file
    plt.close()
