# Real-time Data Visualization with ZeroMQ, PyQt5, and QGIS

## Overview
This project integrates real-time data transmission and visualization using ZeroMQ for message passing, PyQt5 for creating a graphical user interface (GUI), and QGIS for spatial data visualization. It demonstrates a system where data published by one component (publisher) is subscribed to and visualized dynamically in another component (subscriber) within a QGIS map canvas.

## Components
### Publisher (`publisher.py`)
- Uses ZeroMQ's PUB socket to publish data continuously.
- Sends grouped data from a pandas DataFrame over TCP/IP.
- Provides a mechanism for real-time data distribution.

### Subscriber with PyQt5 GUI (`subscriber_gui.py`)
- Implements a PyQt5 application with a QWidget-based GUI.
- Subscribes to data from the publisher via ZeroMQ's SUB socket.
- Displays real-time data updates on a QGIS map canvas.
- Includes features like clearing the display and updating points based on incoming data.

### Subscriber with QGIS Integration (`subscriber_qgis.py`)
- Utilizes QGIS libraries to create a map canvas for visualizing spatial data.
- Subscribes to real-time updates from the publisher using ZeroMQ.
- Updates point features on the map based on incoming data.
- Provides seamless integration of real-time data visualization with spatial analytics.

### Additional Components
- **CSV Reader and Plotter (`csv_reader_plotter.py`)**: Reads CSV data and plots points on a QGIS map, demonstrating initial data setup and visualization.

## Dependencies
- Python 3.x
- PyZMQ (Python bindings for ZeroMQ)
- PyQt5 (for GUI components)
- QGIS Python API (for spatial data handling and visualization)

## Usage
1. **Setup Environment:**
   - Install Python 3.x, `pyzmq`, `pyqt5`, and QGIS.
   - Ensure all dependencies are properly configured.

2. **Run Publisher:**
   - Execute `publisher.py` to start publishing data.

3. **Run Subscriber with GUI:**
   - Execute `subscriber_gui.py` to launch the PyQt5 application with a QGIS map canvas for real-time data visualization.

4. **Run Subscriber with QGIS Integration:**
   - Execute `subscriber_qgis.py` to integrate real-time data updates directly into a QGIS map canvas.

5. **Customization:**
   - Modify data sources, visualization parameters, and GUI layout as per project requirements.
   - Extend functionality for specific use cases involving real-time data analysis and visualization.

## Example Scenario

- The publisher continuously sends grouped data from a CSV file over a ZeroMQ socket.
- Subscribers (GUI and QGIS) receive and visualize real-time updates, demonstrating dynamic data integration with spatial visualization.
