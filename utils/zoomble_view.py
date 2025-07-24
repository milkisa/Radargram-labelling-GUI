from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QWheelEvent, QPainter
from PyQt6.QtCore import Qt

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self,scene, parent=None):
        super().__init__(parent)
        self.setScene(scene)
        self.setScene(QGraphicsScene(self))
        self.image_item = QGraphicsPixmapItem()  # Holds the image
        self.scene().addItem(self.image_item)
        
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Enable panning

        self.zoom_factor = 1.15  # Adjust zoom speed

    def set_image(self, pixmap):
        """ Set the image in the QGraphicsView """
        self.image_item.setPixmap(pixmap)
        self.image_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.setSceneRect(self.image_item.boundingRect())  # Fit scene to image

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out when scrolling mouse wheel """
        zoom_in = event.angleDelta().y() > 0  # Positive scroll = zoom in
        if zoom_in:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
