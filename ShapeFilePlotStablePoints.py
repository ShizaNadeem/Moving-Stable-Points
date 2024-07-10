import sys
from qgis.core import QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

def main():
    """
    Main function to set up and run the QGIS application.
    """
    # Set up the QGIS application environment
    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Create and configure the map canvas
    canvas = QgsMapCanvas()  # QgsMapCanvas is a widget that displays map layers, used to visualize geographical data
    canvas.setCanvasColor(Qt.white)  # Set canvas background color to black

    # Path to the shapefile
    point_path = "D:\CENTAIC WORK (AI BDA)\GIS\PointsPlot-csv (2nd July)\poc shapefile\point_layer.shp"
    world_map = "D:\CENTAIC WORK (AI BDA)\GIS\PointsPlot-csv (2nd July)\poc shapefile\PAK_adm2.shp"
    # Load the vector layer
    pak_layer = QgsVectorLayer(point_path, "Shape File", "ogr")
    pak_layer1 = QgsVectorLayer(world_map, "Shape File", "ogr")
    if not pak_layer.isValid():
        print("Layer failed to load!")
        return

    pak_layer.setOpacity(0.8)  # Set layer opacity
    pak_layer1.setOpacity(0.8)  # Set layer opacity

    # Set up the main window
    main_window = QMainWindow()  #Provides a main application window with standard features like menus, toolbars, and a status bar.
    main_window.setCentralWidget(canvas)  # Set the canvas as the central widget
    main_window.setFixedSize(800, 600)  # Set a fixed size for the window
    main_window.show()

    # Set the extent of the map to focus on the vector layer
    # Ensures that when the map canvas is displayed, it is zoomed and centered to show the entire area covered by the pak_layer.
    canvas.setExtent(pak_layer.extent())
    canvas.setLayers([pak_layer, pak_layer1])

    # Display the canvas
    canvas.show()

    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()