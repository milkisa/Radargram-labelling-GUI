import numpy as np
from PIL import Image
from segment_anything import SamPredictor, sam_model_registry
from utils.lora import inject_lora_into_sam_image_encoder
import torch

MODEL_TYPE = "vit_h"
BASE_SAM_CHECKPOINT = "E:/important/phd/project/new_project/segment_anything/gui/checkpoint/sam_vit_h_4b8939.pth"
LORA_FINETUNED_CHECKPOINT = "E:/important/phd/project/new_project/segment_anything/sam_data/checkpoint/sam_lora_epoch_reduced.pth"

sam = sam_model_registry[MODEL_TYPE](checkpoint=BASE_SAM_CHECKPOINT)

#sam.image_encoder = inject_lora_into_sam_image_encoder(sam.image_encoder, r=8, alpha=16, dropout=0.1)
#sam.load_state_dict(torch.load(LORA_FINETUNED_CHECKPOINT, map_location="cpu"))
predictor = SamPredictor(sam)


import time

def attach_image(self):
    if self.patches:
        self.statusLabel.setText(f"⏳ Attaching patch {self.current_patch_index + 1} / {len(self.patches)}... Please wait. ")  
        self.statusLabel.repaint()  # Force immediate UI update

        start_time = time.time()  # Start timing

        patch = self.patches[self.current_patch_index]
        predictor.set_image(patch)

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time  # Compute elapsed time

        self.image_attached = True  # Enable point selection after attaching
        
        self.segmentButton.setEnabled(True)
        self.clearLastButton.setEnabled(True)
        self.clearAllButton.setEnabled(True)
        self.classSelector.setEnabled(True)  # Enable segmentation button after attaching image
        self.exportButton.setEnabled(True)  # Enable export button after attaching image
        
        self.statusLabel.setText(f"🔗 Patch {self.current_patch_index + 1} / {len(self.patches)} attached in {elapsed_time:.2f} seconds. Select points and then click 'Segment'.")
        print(f"Image attached in {elapsed_time:.2f} seconds.")

    
    
