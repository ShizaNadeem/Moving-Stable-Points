import zmq
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
import pandas as pd
import io
import sys
import os
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.core import QgsMessageLog, Qgis

def plot_points(random_points, point_layer, canvas):
    feats = []
    for coords in random_points:
        feat = QgsFeature(point_layer.fields())
        feat.setAttribute('Longitude', coords[0])
        feat.setAttribute('Latitude', coords[1])
        feat.setAttribute('Identity', coords[2])
        feat.setAttribute('Time', coords[3])
        point = QgsGeometry.fromPointXY(QgsPointXY(coords[0], coords[1]))
        feat.setGeometry(point)
        feats.append(feat)

    point_layer.dataProvider().addFeatures(feats)


def update_canvas(point_layer, canvas):
    # Delete existing points
    feature_ids = [feature.id() for feature in point_layer.getFeatures()]
    point_layer.dataProvider().deleteFeatures(feature_ids)

    # Receive random points from ZeroMQ socket
    message = socket.recv_string()
    print(message)
    time_value, group_csv_data = message.split(' ', 1)
    df = pd.read_csv(io.StringIO(group_csv_data))

    # Extract latitude and longitude from each row
    random_points = [(row['long'], row['lat'], row['Identity'], row['TIME']) for _, row in df.iterrows()]
    # Plot new points
    plot_points(random_points, point_layer, canvas)

    # Refresh the canvas to apply the changes
    canvas.refresh()


if __name__ == '__main__':
    # Create a ZeroMQ context
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:1132")
    socket.subscribe(b"")

    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Set up the map canvas
    canvas = QgsMapCanvas()
    canvas.setCanvasColor(Qt.black)
    canvas.show()

    # Example of adding a vector layer
    layer_path = "./poc shapefile/Map_real_poc.shp"
    vlayer = QgsVectorLayer(layer_path, "Shape File", "ogr")
    vlayer.renderer().symbol().setColor(Qt.green)

    # Create an empty point layer
    point_layer = QgsVectorLayer("Point", "Moving Points", "memory")
    point_layer.renderer().symbol().setColor(Qt.red)
    provider = point_layer.dataProvider()
    fields = QgsFields()
    fields.append(QgsField("Identity", QVariant.Int))  # Add a field named "Field1" of type String
    fields.append(QgsField("Longitude", QVariant.Double))
    fields.append(QgsField("Latitude", QVariant.Double))
    fields.append(QgsField("Time", QVariant.Int))
    provider.addAttributes(fields)
    point_layer.updateFields()

    # Set extent to the extent of the layer
    canvas.setExtent(vlayer.extent())
    # Set the map canvas layer set
    canvas.setLayers([vlayer, point_layer])
    canvas.refresh()

    # Create QTimer to trigger the canvas update every 1 second
    timer = QTimer()
    timer.timeout.connect(lambda: update_canvas(point_layer, canvas))
    timer.start(1000)  # 1000 milliseconds = 1 second

    # Start the application event loop
    sys.exit(app.exec_())