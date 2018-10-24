import subprocess
import os

def sync_files():
    form_dir = "./form/data"
    wp_dir = "./wp/form_data"

    if not os.path.exists(wp_dir):
        os.makedirs(wp_dir)
    
    process = subprocess.call(["rsync", "-avz", form_dir, wp_dir ])

sync_files()
