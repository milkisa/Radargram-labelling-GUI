import numpy as np
from PIL import Image
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
def apply_overlay(self):

        """ Overlay segmentation result on the original patch. """
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

        # Update QLabel with overlaid image
        self.pixmap = QPixmap("overlay_patch.png")
        max_width = self.label.width() * 0.995  # 99.5% of the window width
        max_height = self.label.height() * 0.995  # 99.5% of the window height

        # Scale the pixmap (image) for display purposes while keeping the aspect ratio
        scaled_pixmap = self.pixmap.scaled(int(max_width), int(max_height), 
                                          Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(self.pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
   # self.label.setPixmap(self.pixmap)
    #self.label.setScaledContents(True)
        self.statusLabel.setText(f"📌 Overlay applied to Patch {self.current_patch_index + 1}.")
def remove_overlay(self):
    """Remove the overlay and restore the original patch."""
    if not self.patches:
        return

    patch = self.patches[self.current_patch_index]
    original_image = Image.fromarray(patch)
    original_image.save("original_patch.png")

    # Update QLabel with original image
    self.pixmap = QPixmap("original_patch.png")
    self.label.setPixmap(self.pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
   # self.label.setPixmap(self.pixmap)
    #self.label.setScaledContents(True)

    self.overlay_active = False  # Update overlay state
    self.overlayButton.setText("📌 Overlay Segmentation")  # Reset button text
    self.statusLabel.setText(f"🔄 Overlay removed from Patch {self.current_patch_index + 1}.")