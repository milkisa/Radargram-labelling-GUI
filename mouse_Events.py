from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
def handle_mouse_press(self, event):
        if not self.image_attached:  
            self.statusLabel.setText("⚠️ Please attach the image before selecting points.")
            return  # Do nothing if the image is not attached
        print('okk')
        """ Capture click coordinates and assign them to selected class. """
        if self.image is None or not self.patches:
            print('errror')
            return
        coords = getImageCoordinates(self, event)
        if coords is None:
            return
        x, y = coords
        selected_class = self.classSelector.currentIndex() + 1

        if selected_class not in self.patch_points[self.current_patch_index]:
            self.patch_points[self.current_patch_index][selected_class] = []
        self.patch_points[self.current_patch_index][selected_class].append((x, y))
        self.click_history.append((self.current_patch_index, selected_class, (x, y)))
        print(self.patch_points)
        print(len(self.patch_points))
        print(self.click_history, 'History')
        print(len(self.click_history), 'History')
        self.statusLabel.setText(f"🖱️ Patch {self.current_patch_index + 1}: Class {selected_class} point added.")
        updateImageWithPoints(self)
def updateImageWithPoints(self):
    """ Draws class-colored dots on the image at selected points for the current patch. """
    if self.pixmap:
        temp_pixmap = self.pixmap.copy()
        painter = QPainter(temp_pixmap)

        for class_id, points in self.patch_points[self.current_patch_index].items():
            pen = QPen(self.class_colors[class_id])  # Use predefined colors
            pen.setWidth(10)  # Dot size
            painter.setPen(pen)

            for point in points:
                painter.drawPoint(QPoint(point[0], point[1]))

        painter.end()
        scaled_pixmap = temp_pixmap.scaled(
        self.label.size(),  # Scale to QLabel size
        Qt.AspectRatioMode.KeepAspectRatio,  # Maintain aspect ratio
        Qt.TransformationMode.SmoothTransformation  # Smooth scaling
        )
        self.label.setPixmap(scaled_pixmap)  # Update QLabel with modified image

def getImageCoordinates(self, event):
    """ Convert click position to image coordinates. """
    label_rect = self.label.contentsRect()
    if not self.pixmap:
        return None
    scale_x = self.pixmap.width() / label_rect.width()
    scale_y = self.pixmap.height() / label_rect.height()
    x = int(event.position().x() * scale_x)
    y = int(event.position().y() * scale_y)
    return x, y