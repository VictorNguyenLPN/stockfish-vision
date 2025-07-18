# stockfish-vision/tools/generate_dataset_from_templates.py

import os
import shutil

TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'dataset'

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(TEMPLATE_DIR):
    if filename.endswith(".png"):
        label = filename.split('_')[0]  # e.g., 'wP_1' → 'wP'
        print(f"Processing label: {label}")
        src_path = os.path.join(TEMPLATE_DIR, filename)
        dst_dir = os.path.join(OUTPUT_DIR, label)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(src_path, os.path.join(dst_dir, filename))

print("Dataset generated into:", OUTPUT_DIR)
