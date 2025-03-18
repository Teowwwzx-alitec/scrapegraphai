import os
from datetime import datetime

def create_directories():
    """Create directories for storing artifacts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = "captures"
    dirs = {
        'screenshots': os.path.join(base_dir, timestamp, 'screenshots'),
        'structure': os.path.join(base_dir, timestamp, 'structure'),
        'recordings': os.path.join(base_dir, timestamp, 'recordings')
    }
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    return dirs 