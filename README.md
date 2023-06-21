Lamport Clock
This project implements a visualization of the Lamport logical clock using Python and Tkinter. The Lamport clock algorithm is a logical clock used in distributed systems to order events. The program simulates a server and multiple client events, where the clients send requests to the server, and the server processes them while updating the Lamport clock.

Prerequisites
Before running the program, ensure that you have the following dependencies installed:

Python 3
matplotlib
You can install the dependencies by running the following command:

bash
Copy code
pip install -r requirements.txt
Running the Program
To run the Lamport Clock program, follow these steps:

Clone the project repository:

bash
Copy code
git clone https://github.com/matheuskolln/lamport-clock
Navigate to the project directory:

bash
Copy code
cd lamport-clock
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Run the main.py script:

bash
Copy code
python main.py
The graphical user interface (GUI) window will appear, showing the Lamport Clock program.

Click the "Create a Client" button to add a new client to the server's client list. In the client creation window, enter the event details (event name and execution time) and click "Add Event" to add events to the client. Repeat this step to add multiple events for the client.

Once you have added all the events for a client, click the "Finish" button to save the client to the server. Repeat steps 6 and 7 to add more clients.

Once you have added all the clients and their events, click the "Execute Events" button to start the clock and simulate the execution of the events.

The program will generate a chart visualizing the Lamport clock and the execution of events. The chart will be saved as "chart.png" in the project directory.

Program Structure
main.py: The main script that sets up the GUI, handles button actions, and coordinates the server and client processes.
server.py: Implements the Server class responsible for managing the client list and processing events.
client.py: Implements the Client class that represents the client events and sends requests to the server.
lamport.py: Contains the LamportClock class for tracking the Lamport logical time.
chart.png: The generated chart image file.
