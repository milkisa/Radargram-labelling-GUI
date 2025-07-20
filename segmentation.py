import numpy as np
from PIL import Image
from attach import predictor
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint
from overlay import apply_overlay


from PyQt6.QtWidgets import QApplication, QMessageBox

class SegmentationGUI:
    def __init__(self, parent=None):
        self.parent = parent  # Reference to main application
        self.auto_apply_choice = {}   # Stores the "Apply to All" decision

    def resolve_overlap(self, existing_class, new_class):
        """
        Display a PyQt6 pop-up asking the user which class to keep in case of an overlap.
        Returns the selected class.
        """
        class_pair = tuple(sorted([existing_class, new_class]))
        print(class_pair)

        # If the conflict between these classes has been resolved before, apply the saved choice
        if class_pair in self.auto_apply_choice:
            return self.auto_apply_choice[class_pair]
   

        msg_box = QMessageBox(self.parent)  # Attach to the main application window
        msg_box.setWindowTitle("Class Overlap Detected")
        msg_box.setText(f"Overlap detected!\nExisting Class: {existing_class}\nNew Class: {new_class}\nWhich one should be kept?")
        
        keep_existing = msg_box.addButton(f"Keep class {existing_class}", QMessageBox.ButtonRole.YesRole)
        keep_new = msg_box.addButton(f"Keep class {new_class}", QMessageBox.ButtonRole.NoRole)
       # apply_all = msg_box.addButton("Apply to All", QMessageBox.ButtonRole.RejectRole)
        class_colors = {
        1: "red",
        2: "blue",
        3: "green",
        4: "yellow",
        5: "magenta",
        6: "cyan"
        }

    # Set button colors based on the class
        keep_existing.setStyleSheet(f"background-color: {class_colors[existing_class]}; color: white;")
        keep_new.setStyleSheet(f"background-color: {class_colors[new_class]}; color: white;")
        msg_box.exec()

        if msg_box.clickedButton() == keep_existing:
            self.auto_apply_choice[class_pair] = existing_class  # Remember user choice for future conflicts
            return existing_class
        else:
            self.auto_apply_choice[class_pair] = new_class  # Remember user choice for future conflicts
            return new_class

# Inside your BaseImageSegmentationApp class, modify run_Segmentation:

def run_Segmentation(self):
    """ Perform segmentation on the current patch with user-driven conflict resolution. """
    if not self.patches:
        return
    
    patch = self.patches[self.current_patch_index]
    segmentation_map = np.zeros((patch.shape[0], patch.shape[1]), dtype=np.uint8)
    
    if self.patch_points[self.current_patch_index]:
        self.gui = SegmentationGUI(self)  # Initialize GUI within the main app

        for class_id, points in self.patch_points[self.current_patch_index].items():
            point_coords = np.array(points)
            point_labels = np.ones(len(point_coords), dtype=int)
            masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)

            mask_indices = masks[0] > 0
            for idx in np.where(mask_indices.flatten())[0]:
                existing_class = segmentation_map.flat[idx]

                if existing_class > 0 and existing_class != class_id:
                    chosen_class = self.gui.resolve_overlap(existing_class, class_id)
                    segmentation_map.flat[idx] = chosen_class
                else:
                    segmentation_map.flat[idx] = class_id

    self.stored_segmentation_map = segmentation_map  # Store segmentation result
    
    # Convert segmentation map to a color image
    segmentation_color = np.zeros((patch.shape[0], patch.shape[1], 3), dtype=np.uint8)
    print(np.unique(segmentation_map), 'prediction')

    for class_id, rgb in self.class_rgb.items():
        mask = segmentation_map == class_id
        segmentation_color[mask] = rgb

    segmented_image = Image.fromarray(segmentation_color)
    segmented_image.save("segmentation_patch.png")  # Save segmentation result as a temporary file

    # Update segmentation display in the GUI
    self.segmentationPixmap = QPixmap("segmentation_patch.png")
    self.segmentationDisplay.setPixmap(self.segmentationPixmap.scaled(
        self.segmentationDisplay.size(),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    ))

    self.segmentationDisplay.setScaledContents(True)
    self.overlayButton.setEnabled(True)
    self.statusLabel.setText(f"✅ Segmentation complete for Patch {self.current_patch_index + 1} / {len(self.patches)}!")

def remove_Segmentation(self):
    """Clears the segmentation map"""
    self.segmentationDisplay.clear()


