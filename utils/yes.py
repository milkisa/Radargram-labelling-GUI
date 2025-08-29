from PyQt6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton,
                             QFileDialog, QWidget, QComboBox, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
import sys
import numpy as np
import torch
from segment_anything import SamPredictor, sam_model_registry
from PIL import Image
import pandas as pd
from zoomble_view import ZoomableGraphicsView 
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint


# Load SAM Model
MODEL_TYPE = "vit_h"
CHECKPOINT_PATH = "E:/important/phd/project/new_project/segment_anything/gui/checkpoint/sam_vit_h_4b8939.pth"
sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
predictor = SamPredictor(sam)


class ImageSegmentationApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.image_attached = False  # Prevents point selection before attachment
        self.scene = QGraphicsScene()
        self.view = ZoomableGraphicsView(self.scene)  # Initializing the view once
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Interactive Radar sounder data Segmentation")
        
        # Layout initialization
        self.layout = QVBoxLayout()

        # Image Display Label (Clickable)
        self.layout.addWidget(self.view)

        # Upload Button
        self.uploadButton = QPushButton("📤 Upload Image", self)
        self.uploadButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.uploadButton)

        # Attach Button
        self.attachButton = QPushButton("🔗 Attach", self)
        self.attachButton.setEnabled(True)
        self.attachButton.clicked.connect(self.attachImage)
        self.layout.addWidget(self.attachButton)

        # Class Selector
        self.classSelector = QComboBox(self)
        self.classSelector.addItems(["Class 1", "Class 2", "Class 3", "Class 4"])
        self.layout.addWidget(self.classSelector)
        self.classSelector.setEnabled(False)

        # Clear Button
        self.clearButton = QPushButton("🗑️ Clear Points", self)
        self.clearButton.clicked.connect(self.clearPoints)
        self.layout.addWidget(self.clearButton)
        self.clearButton.setEnabled(False)

        # Status Label
        self.statusLabel = QLabel("No image loaded.", self)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.statusLabel)

        # Segmentation Display Label
        self.segmentationDisplay = QLabel(self)
        self.segmentationDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.segmentationDisplay)

        # Navigation Buttons
        self.patchNavLayout = QHBoxLayout()
        self.prevPatchButton = QPushButton("⬅ Prev Patch", self)
        self.nextPatchButton = QPushButton("Next Patch ➡", self)
        self.prevPatchButton.clicked.connect(self.prevPatch)
        self.nextPatchButton.clicked.connect(self.nextPatch)
        self.patchNavLayout.addWidget(self.prevPatchButton)
        self.patchNavLayout.addWidget(self.nextPatchButton)
        self.layout.addLayout(self.patchNavLayout)

        # Segment Button
        self.segmentButton = QPushButton("🚀 Run Segmentation", self)
        self.segmentButton.clicked.connect(self.runSegmentation)
        self.layout.addWidget(self.segmentButton)
        self.segmentButton.setEnabled(False)

        # Overlay Button
        self.overlayButton = QPushButton("📌 Overlay Segmentation", self)
        self.overlayButton.clicked.connect(self.overlaySegmentation)
        self.layout.addWidget(self.overlayButton)
        self.overlayButton.setEnabled(False)

        # Set layout
        self.setLayout(self.layout)

        # Image & Patching Variables
        self.image = None
        self.pixmap = None
        self.patches = []
        self.current_patch_index = 0
        self.patch_points = [{} for _ in range(len(self.patches))]  # Initialize patch points
        self.class_colors = {
            1: Qt.GlobalColor.red,
            2: Qt.GlobalColor.blue,
            3: Qt.GlobalColor.green,
            4: Qt.GlobalColor.yellow,
        }
        # RGB mapping for final segmentation visualization
        self.class_rgb = {
            1: (255, 0, 0),
            2: (0, 0, 255),
            3: (0, 255, 0),
            4: (255, 255, 0),
        }


    def loadImage(self):
        """ Load an image and divide it into patches. """
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg);;CSV Files (*.csv)")
        
        if filePath:
            try:
                if filePath.endswith('.csv'):
                    # Assuming that the CSV file contains image data
                    image_all = pd.read_csv(filePath, header=None).to_numpy()
                    # Normalize the image data to be between 0 and 1
                    rs = (image_all - image_all.min()) / (image_all.max() - image_all.min())
                    # Stack the image into RGB channels
                    print(rs.shape)
                    rs = (rs * 255)
                    self.image = np.array(np.stack([rs] * 3, axis=-1)).astype(np.uint8)
                    print(self.image.shape)
                  
                else:
                    # Load and convert the image to RGB
                    self.image = np.array(Image.open(filePath).convert("RGB")).astype(np.uint8)
                    
                
                self.divideIntoPatches()
                self.displayCurrentPatch()
                self.statusLabel.setText("✅ Please attach the image to the model.")
            
            except Exception as e:
                self.statusLabel.setText(f"❌ Error loading image: {str(e)}")
        else:
            self.statusLabel.setText("❌ No file selected.")

    def divideIntoPatches(self):
        """ Divide image into patches of 500px width. """
        patch_size=2000
        if self.image.shape[1] > patch_size:
            num_patches = int(self.image.shape[1] / patch_size)
            self.patches = [self.image[:, i * patch_size:(i + 1) * patch_size] for i in range(num_patches)]
        else:
            self.patches = [self.image]
        self.patch_points = [{} for _ in range(len(self.patches))]
        self.current_patch_index = 0

    def displayCurrentPatch(self):
        """ Display the currently selected patch. """
        if self.patches:
            patch = self.patches[self.current_patch_index]
            image = Image.fromarray(patch)
            image.save("temp_patch.png")
            self.pixmap = QPixmap("temp_patch.png")
            self.view.set_image(self.pixmap)
            
           #self.label.setScaledContents(True)
            self.click_points = {i: [] for i in range(1, 5)}  # Reset points
           # self.label.update()


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
    def clearPoints(self):
        """ Clears all selected points and refreshes the displayed image. """
        # Reset the points for the current patch
        self.patch_points[self.current_patch_index] = {}

        # Reset the status label
        self.statusLabel.setText("🗑️ All points cleared. Select new points for segmentation.")

        # Update the image with the cleared points
        self.updateImageWithPoints()

        # Reset the view to the original image (without points)
        if self.pixmap:
            # Ensure that the view is showing the unmodified image
            self.view.set_image(self.pixmap)  # Reset the view to the original image

        # Update the status label to indicate that the points are cleared
        self.statusLabel.setText("🗑️ Points cleared. Please add new points for segmentation.")

    def mousePressEvent(self, event):
        """ Capture click coordinates and assign them to selected class within ZoomableGraphicsView. """
        if not self.image_attached:  
            self.statusLabel.setText("⚠️ Please attach the image before selecting points.")
            print("No image attached")
            return  # Do nothing if the image is not attached

        if self.image is None or not self.patches:
            return

        # Convert click position to scene coordinates (considering zoom level)
        scene_coords = self.view.mapToScene(event.pos()).toPoint()  # Scene coordinates after zoom
        print(f"Scene coordinates: {scene_coords}")

        # Get the current zoom scale factors from the view
        scale_x = self.view.transform().m11()  # Scale factor in the x-direction
        scale_y = self.view.transform().m22()  # Scale factor in the y-direction
        print(f"Zoom scale factors: scale_x={scale_x}, scale_y={scale_y}")

        # Get the image item from the scene
        image_item = self.view.image_item  # Assuming the image is added to the scene as an item
        if not image_item:
            print("No image item found in the scene")
            return

        # Get the image's top-left corner position in the scene
        image_pos = image_item.pos()  # This gives the scene coordinates of the top-left corner of the image
        print(f"Image position in scene: {image_pos}")

        # Adjust scene coordinates by the image's position to get coordinates relative to the image
        image_relative_x = scene_coords.x() - image_pos.x()
        image_relative_y = scene_coords.y() - image_pos.y()

        print(f"Relative coordinates within image (before zoom): ({image_relative_x}, {image_relative_y})")

        # Now, apply the inverse of the zoom scale to get the coordinates in the original image's dimensions
        image_x = int(image_relative_x )  # Adjust based on zoom scale
        image_y = int(image_relative_y )  # Adjust based on zoom scale

        print(f"Adjusted coordinates in image (after scaling): ({image_x}, {image_y})")

        # Ensure coordinates are within valid bounds of the current patch
        patch = self.patches[self.current_patch_index]
        if image_x < 0 or image_y < 0 or image_x >= patch.shape[1] or image_y >= patch.shape[0]:
            print(f"Coordinates out of bounds: ({image_x}, {image_y})")
            return

        # Get the selected class from the combo box (user-selected class)
        selected_class = self.classSelector.currentIndex() + 1
        print(f'Class label: {selected_class}, Coordinates: ({image_x}, {image_y})')

        # Store the selected point in the current patch
        if selected_class not in self.patch_points[self.current_patch_index]:
            self.patch_points[self.current_patch_index][selected_class] = []
        self.patch_points[self.current_patch_index][selected_class].append((image_x, image_y))
        print(f"Points for class {selected_class}: {self.patch_points[self.current_patch_index][selected_class]}")

        # Update the status label to show feedback to the user
        self.statusLabel.setText(f"🖱️ Patch {self.current_patch_index + 1}: Class {selected_class} point added.")

        # Update the image with the new points
        self.updateImageWithPoints()


    def updateImageWithPoints(self):
        """ Update the image in the QGraphicsView with the current points. """
        if self.image is None:
            return

        # Create a copy of the image to draw the points on it
        temp_pixmap = self.pixmap.copy()

        # Get the painter for drawing on the pixmap
        painter = QPainter(temp_pixmap)
        painter.setPen(Qt.GlobalColor.black)  # Set pen color for the points
        painter.setBrush(Qt.GlobalColor.red)  # Set brush for filling points

        # Loop over all patches and classes to draw points
        for class_id, points in self.patch_points[self.current_patch_index].items():
            for point in points:
                painter.drawEllipse(point[0] - 3, point[1] - 3, 6, 6)  # Draw a small circle at the point

        painter.end()  # End the drawing process

        # Update the pixmap in the QGraphicsView
        self.view.set_image(temp_pixmap)  # Assuming `set_image` is defined in ZoomableGraphicsView





    def getImageCoordinates(self, event):
        if not self.view.image_item.pixmap():
            return None

        # Convert scene coordinates to image coordinates
        scene_pos = self.view.mapToScene(event.pos())
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        return x, y
    def attachImage(self):
        """ Attach the current patch to the predictor. """
        
        if self.patches:
            self.statusLabel.setText("⏳ Attaching image... Please wait.")  
            self.statusLabel.repaint()  # Force immediate UI update

            patch = self.patches[self.current_patch_index]
            predictor.set_image(patch)
            self.image_attached = True  # Enable point selection after attaching
            
            self.segmentButton.setEnabled(True)
            self.clearButton.setEnabled(True)
            self.classSelector.setEnabled(True)  # Enable segmentation button after attaching image
            self.statusLabel.setText("🔗 Image attached. Select points and then click 'Segment'.")
            
    def runSegmentation(self):
            """ Perform segmentation on the current patch. """
            if not self.patches:
                return
            patch = self.patches[self.current_patch_index]
            segmentation_map = np.zeros((patch.shape[0], patch.shape[1]), dtype=np.uint8)

            if self.patch_points[self.current_patch_index]:
            
              
                for class_id, points in self.patch_points[self.current_patch_index].items():
                    point_coords = np.array(points)
                    point_labels = np.ones(len(point_coords), dtype=int)
                    masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)
                    segmentation_map[masks[0] > 0] = class_id
            self.stored_segmentation_map = segmentation_map  # Store segmentation result
            segmentation_color = np.zeros((patch.shape[0], patch.shape[1], 3), dtype=np.uint8)
            print(np.unique(segmentation_map), 'predicion')
            for class_id, rgb in self.class_rgb.items():
                mask = segmentation_map == class_id
                segmentation_color[mask] = rgb
            segmented_image = Image.fromarray(segmentation_color)

            segmented_image.save("segmentation_patch.png")  # Save as temp file

            # Update segmentation display in the GUI
            self.segmentationPixmap = QPixmap("segmentation_patch.png")
            self.segmentationDisplay.setPixmap(self.segmentationPixmap)
           # self.segmentationDisplay.setScaledContents(True)
            self.overlayButton.setEnabled(True)

            self.statusLabel.setText(f"✅ Segmentation complete for Patch {self.current_patch_index + 1}!")
    def overlaySegmentation(self):
        """ Overlay segmentation result on the original patch using ZoomableGraphicsView. """
        if not self.patches or self.stored_segmentation_map is None:
            self.statusLabel.setText("⚠️ Run segmentation first before applying overlay.")
            return

        patch = self.patches[self.current_patch_index]

        segmentation_map = self.stored_segmentation_map

        segmentation_color = np.zeros((patch.shape[0], patch.shape[1], 3), dtype=np.uint8)
        for class_id, rgb in self.class_rgb.items():
            mask = segmentation_map == class_id
            segmentation_color[mask] = rgb

        # Blend original image and segmentation result
        overlay = (0.5 * patch + 0.5 * segmentation_color).astype(np.uint8)
        overlay_image = Image.fromarray(overlay)
        overlay_image.save("overlay_patch.png")

        # Display the overlay using ZoomableGraphicsView
        overlay_pixmap = QPixmap("overlay_patch.png")
        self.view.set_image(overlay_pixmap)

        self.statusLabel.setText(f"📌 Overlay applied to Patch {self.current_patch_index + 1}.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSegmentationApp()
    window.show()
    sys.exit(app.exec())
