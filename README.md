# Lamport Clock

This project implements a visualization of the Lamport logical clock using Python and Tkinter. The Lamport clock algorithm is a logical clock used in distributed systems to order events. The program simulates a server and multiple client processes, where the clients send requests to the server, and the server processes them while updating the Lamport clock.

## Prerequisites

Before running the program, ensure that you have the following dependencies installed:

- Python 3
- matplotlib
- Pillow

You can install the dependencies by running the following command:

```
pip install -r requirements.txt
```

## Running the Program

To run the Lamport Clock program, follow these steps:

1. Clone the project repository:

   ```
   git clone https://github.com/matheuskolln/lamport-clock
   ```

2. Navigate to the project directory:

   ```
   cd lamport-clock
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the main.py script:

   ```
   python main.py
   ```

5. The graphical user interface (GUI) window will appear, showing the Lamport Clock program.

6. Click the "Add Process" button to add a new process to the server's process list.

7. Once you have added the desired processes, click the "Run Clock" button to start the clock and simulate the execution of the processes.

8. The chart will be dynamically updated to visualize the Lamport clock and the execution of processes.

9. To reset the clock and clear the process list, click the "Reset" button.

## Program Structure

- `main.py`: The main script that sets up the GUI, handles button actions, and coordinates the server and client processes.
- `chart.py`: Contains the logic for generating and updating the chart visualization using matplotlib.
- `server.py`: Implements the Server class responsible for managing the process list and processing requests.
- `client.py`: Implements the Client class that represents the client processes and sends requests to the server.
- `lamport.py`: Contains the LamportClock class for tracking the Lamport logical time.
- `chart.png`: The generated chart image file.
