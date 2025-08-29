import torch
import os
from pathlib import Path
import torch
import os
def  export_labels(self):
    """ Export the segmentation labels to a file. """
    # Assuming 'segmentation_labels' holds the result of the segmentation
    # Convert the segmentation labels to a PyTorch tensor (if not already)
    

    if self.loadedFilePath and self.loadedFileName:
        # Create a new file name by appending '_labels' to the original file name (before extension)
        loaded_path = Path(self.loadedFilePath).resolve()

        # Parse base 
        base_name, ext = os.path.splitext(self.loadedFileName)
        #base_name = loaded_path.stem  # e.g., 'Data_img_03_20140521_01_017'
        parts = base_name.split("_")
        folder_name = "_".join(parts[:-1])  # 'Data_img_03_20140521_01'
        new_filename = parts[-1]            # '017'
        print(f"Base name: {base_name}, Folder name: {folder_name}, New filename: {new_filename}")
        print(self.stored_segmentation_map.shape,'self.segmentation_map.shape')
        # Check if the segmentation map is empty
        # Create a new directory for the labels
        # File names
        export_file_name = f"{new_filename}_index_{self.current_patch_index}_labels_len_{self.stored_segmentation_map.shape[1]}.pt"
        label_export_path = loaded_path / folder_name / export_file_name
        data_export_path = loaded_path /  folder_name / f"{new_filename}_index_{self.current_patch_index}_data_len_{self.stored_segmentation_map.shape[1]}.pt"

        # Make directories
        label_export_path.parent.mkdir(parents=True, exist_ok=True)
        data_export_path.parent.mkdir(parents=True, exist_ok=True)

        # Save
        labels_tensor = torch.tensor(self.stored_segmentation_map)
        data_tensor = torch.tensor(self.patches[self.current_patch_index])
        torch.save(labels_tensor, str(label_export_path))
        torch.save(data_tensor, str(data_export_path))



        # You can add a confirmation message or feedback to the user
        print(f"Labels exported to {label_export_path}")
        # Optionally, disable the export button if needed
        self.exportButton.setEnabled(False)
    else:
        print("No file loaded. Cannot export labels.")