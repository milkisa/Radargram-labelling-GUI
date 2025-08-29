from PIL import Image
import numpy as np
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QInputDialog

def divide_into_patches(self, image):
    """ Divide image into patches of 500px width. """
    if image.shape[1] > self.suggested_size:
        width, height = self.image.shape[1], self.image.shape[0]  # Assuming self.image is a NumPy array

    
        suggested_size = 500  # Recommended size
        
        max_patch_size, ok = QInputDialog.getInt(
            self,
            "Set Patch Size",
            "The radiogram is large. Enter the  maximum Horizontal patch size (Recommended: 500 to 1000):",
            value=suggested_size,  # Default value
            min=100,  # Minimum allowed size
            max=width,  # Maximum allowed size (cannot be larger than image width)
            step=50  # Increment step
        )

        if not ok:  # If user cancels, use recommended size
            max_patch_size= suggested_size
    
            
        self.prevPatchButton.setEnabled(True)
        self.nextPatchButton.setEnabled(True)
        print('more thant 500', max_patch_size)
        num_patches = int(image.shape[1] / max_patch_size)
        patches = [image[:, i * max_patch_size:(i + 1) * max_patch_size] for i in range(num_patches)]
    else:
        max_patch_size= None  # No limit
        patches = [image]
    patch_points = [{} for _ in range(len(patches))]
    return patches, patch_points

def display_current_patch(label, patches, current_patch_index):
    """ Display the currently selected patch. """
    if patches:
        
        patch = patches[current_patch_index]
        image = Image.fromarray(patch)
        image.save("temp_patch.png")
        pixmap = QPixmap("temp_patch.png")
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.update()
        return pixmap
