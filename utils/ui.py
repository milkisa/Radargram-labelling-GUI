from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QHBoxLayout,QMainWindow
)
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QIcon
from PIL import Image
import numpy as np


class BaseImageSegmentationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_attached = False  # Prevents point selection before attachment


    def initUI(self):
        self.stored_segmentation_map = None  # To store the last computed segmentation mask

        self.setWindowTitle("Interactive Radar sounder data Segmentation")
        self.setWindowIcon(QIcon("E:/important/phd/project/new_project/segment_anything/RS_GUI/rs_icon.png"))  # Set application icon (replace with your icon path)
        
        self.setStyleSheet("""
   
    
            QWidget {
                background-color: #00194c;
                color: #feec95;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #041469;
                color: #feec95;
           
            }
            QPushButton:hover {
                background-color: #505356;
            }
            QPushButton:disabled {
                background-color: #2a2d2e;  /* Darker shade for inactive buttons */
                color: #777777;  /* Gray text for disabled buttons */
             
            }
            QLabel {
                background-color: #00194c;
                
              
           
            }
            QComboBox:disabled {
                background-color: #2a2d2e;  /* Darker shade for inactive buttons */
                color: #777777;
           
            }
            QComboBox {
                background-color: #041469;
                color: #feec95;
           
            }
            
        """)
        
        
        self.layout = QVBoxLayout()
      

        # Image Display Label (Clickable)
        self.label = QLabel("Upload an Image", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.label, stretch=1)
        

        # Upload Button
        self.uploadButton = QPushButton("📤 Upload Image", self)
        self.uploadButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.uploadButton)

        # patch selector
        self.patchNavLayout = QHBoxLayout()
        self.prevPatchButton = QPushButton("⬅ Prev Patch", self)
        self.nextPatchButton = QPushButton("Next Patch ➡", self)
        self.prevPatchButton.clicked.connect(self.prevPatch)
        self.nextPatchButton.clicked.connect(self.nextPatch)
        self.prevPatchButton.setEnabled(False)
        self.nextPatchButton.setEnabled(False)
        self.patchNavLayout.addWidget(self.prevPatchButton)
        self.patchNavLayout.addWidget(self.nextPatchButton)
        self.layout.addLayout(self.patchNavLayout)

        self.attachButton = QPushButton("🔗 Attach", self)
        self.attachButton.setEnabled(True)
        self.attachButton.clicked.connect(self.attachImage)
        self.layout.addWidget(self.attachButton)
       

        # Class Selector
        self.classSelector = QComboBox(self)
        self.classSelector.addItems(["Class 1 (red)", "Class 2 (blue)", "Class 3 (green)", "Class 4 (yellow)", "Class 5 (purple)", "class 6 (cyan)"])
    
        self.layout.addWidget(self.classSelector)
        self.classSelector.setEnabled(False)
        

        # clear points
        buttonLayout = QHBoxLayout()
        self.clearLastButton = QPushButton("Clear Last Point", self)
        self.clearLastButton.clicked.connect(self.clearLastPoint)

        self.clearAllButton = QPushButton("Clear All Points", self)
        self.clearAllButton.clicked.connect(self.clearAllPoints)
        self.clearLastButton.setEnabled(False)
        self.clearAllButton.setEnabled(False)
        
        buttonLayout.addWidget(self.clearLastButton)
        buttonLayout.addWidget(self.clearAllButton)
        self.layout.addLayout(buttonLayout) 

        # Status Label
        self.statusLabel = QLabel("No image loaded.", self)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.statusLabel)
        self.segmentationDisplay = QLabel(self)
        self.segmentationDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.segmentationDisplay, stretch=1)  # Add below the main image
        

        # Segment Button
        self.segmentButton = QPushButton("🚀 Run Segmentation", self)
        self.segmentButton.clicked.connect(self.toggleSegmetnation)
        self.layout.addWidget(self.segmentButton)
        self.segmentButton.setEnabled(False)

                # Export Button
        self.exportButton = QPushButton("📤 Export Labels", self)
        self.exportButton.clicked.connect(self.exportLabels)
        self.layout.addWidget(self.exportButton)
        self.exportButton.setEnabled(False)  # Initially disable the export button

        # Overlay Button
        self.overlayButton = QPushButton("📌 Overlay Segmentation", self)
        self.overlayButton.clicked.connect(self.toggleOverlay)
        self.layout.addWidget(self.overlayButton)
        self.overlayButton.setEnabled(False)  # Initially disabled
    # Segmentation Display Label



        # Navigation Buttons



        self.setLayout(self.layout)
  
    """
        self.updateLabelSize()
    
    def resizeEvent(self, event):
         Handle window resizing events and update the QLabel size 
        # Update the size whenever the window is resized
        self.updateLabelSize()

        # Call the default resizeEvent handling
        super().resizeEvent(event)
     
    def updateLabelSize(self):
     
        window_width = self.width()
        window_height = self.height()

        # Calculate new size based on a percentage of the window size
        label_width = int(window_width * 0.9)  # 90% width of the window
        label_height = int(window_height * 0.4)  # 30% height of the window

        self.label.setFixedSize(label_width, label_height)
                # Image & Patching Variables
        
    """  

