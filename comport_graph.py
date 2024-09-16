pip install pyserial matplotlib

import serial
import matplotlib.pyplot as plt
from threading import Thread
from queue import Queue

# Global variables for data storage
data_queue_1 = Queue()
data_queue_2 = Queue()

# Function to read data from COM port and store it in a queue
def read_data(serial_port, data_queue):
    try:
        ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_queue.put(float(line))
    except Exception as e:
        print(f"Error reading data from {serial_port}: {e}")

# Function to plot data
def plot_data():
    plt.ion()  # Turn on interactive mode for live updating
    fig, ax = plt.subplots()

    x_data = []
    y_data_1 = []
    y_data_2 = []

    while True:
        try:
            if not data_queue_1.empty() and not data_queue_2.empty():
                x_data.append(len(x_data) + 1)
                y_data_1.append(data_queue_1.get())
                y_data_2.append(data_queue_2.get())

                ax.clear()
                ax.plot(x_data, y_data_1, label='COM Port 1')
                ax.plot(x_data, y_data_2, label='COM Port 2')

                ax.legend()
                ax.set_title('Data from COM Ports')
                ax.set_xlabel('Time')
                ax.set_ylabel('Value')

                plt.draw()
                plt.pause(0.1)  # Adjust the pause time as needed
        except Exception as e:
            print(f"Error plotting data: {e}")

# Main function
def main():
    port1 = 'COM3'  # Change this to the first COM port you want to read from
    port2 = 'COM2'  # Change this to the second COM port you want to read from

    # Create threads for reading data from each COM port
    thread1 = Thread(target=read_data, args=(port1, data_queue_1))
    thread2 = Thread(target=read_data, args=(port2, data_queue_2))

    # Create a thread for plotting data
    plot_thread = Thread(target=plot_data)

    # Start the threads
    thread1.start()
    thread2.start()
    plot_thread.start()

    # Wait for threads to finish (which they won't in this case)
    thread1.join()
    thread2.join()
    plot_thread.join()

if __name__ == "__main__":
    main()
