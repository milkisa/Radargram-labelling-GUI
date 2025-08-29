
from utils.mouse_Events import handle_mouse_press, updateImageWithPoints

def clear_LastPoint(self):
    if not self.click_history:
        self.statusLabel.setText("⚠️ No points to remove.")
        return

    # Get last clicked point from history
    last_patch, last_class, last_point = self.click_history.pop()

    # Remove point from patch list
    
    if last_point in self.patch_points[last_patch][last_class]:  
        self.patch_points[last_patch][last_class].remove(last_point)  # Remove only this point

        # If no points left in this class, remove the class
        if not self.patch_points[last_patch][last_class]:
            del self.patch_points[last_patch][last_class]

        self.statusLabel.setText(f"❌ Last clicked point {last_point} removed.")
        updateImageWithPoints(self)  # Refresh the image display
    else:
        self.statusLabel.setText("⚠️ Point already removed.")
 
        

    """ Removes the last clicked point from the current patch. """
    
    """
    last_label = list(self.patch_points[self.current_patch_index].keys())[-1]  # Get the last used label
    if self.patch_points[self.current_patch_index][last_label]:  # Check if the label has points
        self.patch_points[self.current_patch_index][last_label].pop()  # Remove the last point
        
        if not self.patch_points[self.current_patch_index][last_label]:  # If empty, remove the label
            del self.patch_points[self.current_patch_index][last_label]
        
        self.statusLabel.setText(f"❌ Last point removed. {sum(len(v) for v in self.patch_points[self.current_patch_index].values())} points remaining.")
        updateImageWithPoints(self)  # Refresh the image display
    else:
        self.statusLabel.setText("⚠️ No points to remove.")
    """



def clear_AllPoints(self):
    """ Clears all selected points and refreshes the displayed image. """
    
    self.patch_points[self.current_patch_index] = {}  # Reset points
    self.statusLabel.setText("🗑️ All points cleared. Select new points for segmentation.")
    updateImageWithPoints(self)  # Refresh the display
