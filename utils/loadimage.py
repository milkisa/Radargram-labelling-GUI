import numpy as np
import pandas as pd
from PIL import Image
import pandas as pd
import numpy as np
from PIL import Image
import torch
import os

def load_image(self):
    if self.filePath:
        try:
            if self.filePath.endswith('.csv'):
                # Load from CSV
                image_all = pd.read_csv(self.filePath, header=None).to_numpy()
                rs = (image_all - image_all.min()) / (image_all.max() - image_all.min())
                rs = (rs * 255)
                self.image = np.array(np.stack([rs] * 3, axis=-1)).astype(np.uint8)
                print(self.image.shape)
                self.statusLabel.setText("✅ Radargram loaded from CSV.")
                self.loadedFilePath = os.path.dirname(self.filePath)  # Get directory of the file
                self.loadedFileName = os.path.basename(self.filePath)  # Get the file name without path

            elif self.filePath.endswith('.pt'):
                # Load from PyTorch tensor file
                tensor = torch.load(self.filePath, weights_only=False)
                if isinstance(tensor, torch.Tensor):
                    rs = tensor.numpy()
                elif isinstance(tensor, np.ndarray):
                    rs = tensor
                else:
                    raise ValueError("The .pt file does not contain a supported data type (Tensor or NumPy array).")
    

                # Normalize
                print(rs, 'detecteddddddddddddddddddddddddddddddddd')
                rs = (rs - rs.min()) / (rs.max() - rs.min())
                rs = (rs * 255)
                self.image = np.array(np.stack([rs] * 3, axis=-1)).astype(np.uint8)
                print(self.image.shape)
                self.statusLabel.setText("✅ Radargram loaded from .pt file.")
                self.loadedFilePath = os.path.dirname(self.filePath)  # Get directory of the file
                self.loadedFileName = os.path.basename(self.filePath)  # Get the file name without path

            else:
                # Load and convert standard image
                self.image = np.array(Image.open(self.filePath).convert("RGB")).astype(np.uint8)
                self.statusLabel.setText("✅ Radargram loaded from image.")

        except Exception as e:
            self.statusLabel.setText(f"❌ Error loading image: {str(e)}")
    else:
        self.statusLabel.setText("❌ No file selected.")
