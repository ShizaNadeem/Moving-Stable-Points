import sys
import zmq
import csv
from qgis.core import QgsApplication, QgsVectorLayer, QgsPointXY, QgsGeometry, QgsFeature, QgsFields, QgsField, QgsProject
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QColor
import threading

def read_csv(file_path):
    """
    Read CSV file and return a list of point features.
    """
    features = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            feature = QgsFeature()
            point = QgsPointXY(float(row['long']), float(row['lat']))
            feature.setGeometry(QgsGeometry.fromPointXY(point))
            feature.setAttributes([row['Identity']])
            features.append(feature)
    return features

def main():
    """
    Main function to set up and run the QGIS application.
    """
    # Set up the QGIS application environment
    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Create and configure the map canvas
    canvas = QgsMapCanvas()
    canvas.setCanvasColor(Qt.black)

    # Path to the shapefile
    layer_path = "./poc shapefile/world_map.shp"

    # Load the vector layer
    pak_layer = QgsVectorLayer(layer_path, "Shape File", "ogr")
    if not pak_layer.isValid():
        print("Layer failed to load!")
        return

    pak_layer.setOpacity(0.2)

    # Set up the main window
    main_window = QMainWindow()
    main_window.setCentralWidget(canvas)
    main_window.setFixedSize(800, 600)
    main_window.show()

    # Set the extent of the map to focus on the vector layer
    canvas.setExtent(pak_layer.extent())
    canvas.setLayers([pak_layer])

    # Add point layer for CSV data
    point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "Points", "memory")
    point_layer.startEditing()
    point_layer.dataProvider().addAttributes([QgsField("id", QVariant.String)])
    point_layer.updateFields()

    # Read initial points from CSV
    csv_points = read_csv("selected_rows.csv")
    point_layer.dataProvider().addFeatures(csv_points)
    point_layer.commitChanges()

    # Set point layer style
    symbol = point_layer.renderer().symbol()
    symbol.setColor(QColor("red"))
    symbol.setSize(5)

    # Add point layer to map
    QgsProject.instance().addMapLayer(point_layer)
    canvas.setLayers([pak_layer, point_layer])
    canvas.refresh()

    # ZeroMQ setup
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def update_points():
        while True:
            message = socket.recv_string()
            print(f"Received message: {message}")
            id, longitude, latitude = message.split(",")
            longitude = float(longitude)
            latitude = float(latitude)
            point_layer.startEditing()
            updated = False
            for feature in point_layer.getFeatures():
                if feature['id'] == id:
                    print(f"Updating feature with id: {id}")
                    point_layer.changeGeometry(feature.id(), QgsGeometry.fromPointXY(QgsPointXY(longitude, latitude)))
                    updated = True
                    break
            if updated:
                point_layer.commitChanges()
                canvas.refresh()
                print(f"Feature with id {id} updated to new location: ({longitude}, {latitude})")
            else:
                print(f"No feature found with id: {id}")

    # Start a thread to handle ZeroMQ messages
    zmq_thread = threading.Thread(target=update_points)
    zmq_thread.start()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
