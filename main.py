import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QInputDialog
from ui import BaseImageSegmentationApp
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout)
from PyQt6.QtCore import Qt, QPoint
from ui import BaseImageSegmentationApp
from attach import  attach_image

from patch_manager import divide_into_patches, display_current_patch  # Import new functions
from mouse_Events import handle_mouse_press, updateImageWithPoints
from segmentation import run_Segmentation, remove_Segmentation
from overlay import apply_overlay, remove_overlay
from loadimage import load_image
from clear import clear_AllPoints,clear_LastPoint
from export import export_labels
from PIL import Image
import numpy as np
import pandas as pd
class ImageSegmentationApp(BaseImageSegmentationApp):
    def __init__(self):
        super().__init__()

        self.image_attached = False  # Prevents point selection before attachment


        self.image = None
        self.pixmap = None
        self.filepath= None
        self.suggested_size=500
        self.patches = []
        self.click_history = []  # Track the order of clicked points
        self.current_patch_index = 0
        self.patch_points = []  # Stores points for each patch
        self.class_colors = {
            1: Qt.GlobalColor.red,
            2: Qt.GlobalColor.blue,
            3: Qt.GlobalColor.green,
            4: Qt.GlobalColor.yellow,
            5: Qt.GlobalColor.magenta,
            6: Qt.GlobalColor.cyan,
        }
        # RGB mapping for final segmentation visualization
        self.class_rgb = {
            1: (255, 0, 0),      # Red
            2: (0, 0, 255),      # Blue
            3: (0, 255, 0),      # Green
            4: (255, 255, 0),    # Yellow
            5: (128, 0, 128),    # Purple
            6: (0, 255, 255),    # Light Cyan (changed)
        }
        self.segmentation_result= []
        
    def loadImage(self):
        """ Load an image and divide it into patches. """
        self.filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Radargram",
            "",
            "Supported Files (*.csv *.png *.jpg *.jpeg *.pt);;All Files (*)"
        )

        load_image(self)  # This now handles .csv, .pt, and image files

        self.patches, self.patch_points = divide_into_patches(self, self.image)
        self.displayCurrentPatch()

        


    def displayCurrentPatch(self):
        """ Display the currently selected patch. """
        self.statusLabel.setText(f" ✅  Press the attach button to attach the patch {self.current_patch_index + 1} / {len(self.patches)}  to the model.")
        self.pixmap = display_current_patch(self.label, self.patches, self.current_patch_index)  # Use the new function
        self.label.setPixmap(self.pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
    

    
    def clearAllPoints(self):
            clear_AllPoints(self)
    def clearLastPoint(self):
            clear_LastPoint(self)

    def prevPatch(self):
        """ Navigate to the previous patch. """
        if self.current_patch_index > 0:

            self.current_patch_index -= 1
            self.displayCurrentPatch()

    def nextPatch(self):
        """ Navigate to the next patch. """
        if self.current_patch_index < len(self.patches) - 1:
            self.current_patch_index += 1
            self.displayCurrentPatch()
    
    
    
    def mousePressEvent(self, event):

        handle_mouse_press(self,event)


    
    def attachImage(self):
        """ Attach the current patch to the predictor. """
        

        attach_image(self)
            
            
    def toggleSegmetnation(self):
        if self.segmentButton.text() == "🚀 Run Segmentation":
            run_Segmentation(self) # Call overlay function
            self.segmentButton.setText("❌ Clear Segmentation")
        else:
            remove_Segmentation(self)  # Call function to remove overlay
            self.segmentButton.setText("🚀 Run Segmentation")

            
    def toggleOverlay(self):
        if self.overlayButton.text() == "📌 Overlay Segmentation":
            apply_overlay(self) # Call overlay function
            self.overlayButton.setText("❌ Remove Overlay")
        else:
            remove_overlay(self)  # Call function to remove overlay
            self.overlayButton.setText("📌 Overlay Segmentation")
    def exportLabels(self):
        # Assuming 'segmentation_labels' holds the result of the segmentation
        # Convert the segmentation labels to a PyTorch tensor (if not already)
        export_labels(self)  # Call the export function from the export module


            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSegmentationApp()
    window.show()
    sys.exit(app.exec())
