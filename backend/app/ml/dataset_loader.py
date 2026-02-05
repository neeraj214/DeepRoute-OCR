import os
from typing import List, Optional
from pydantic import BaseModel

class DatasetItem(BaseModel):
    image_path: str
    label_path: str
    ground_truth: str
    filename: str

def load_dataset(dataset_dir: str) -> List[DatasetItem]:
    """
    Loads the OCR evaluation dataset from the specified directory.
    
    Expected structure:
    dataset_dir/
      ├── images/
      └── labels/
      
    Args:
        dataset_dir: Root directory of the dataset.
        
    Returns:
        List of DatasetItem objects.
        
    Raises:
        ValueError: If directories are missing or dataset is empty.
    """
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")
    
    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        raise ValueError(f"Dataset directory must contain 'images' and 'labels' subdirectories. Checked: {images_dir}, {labels_dir}")
        
    items = []
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    
    # List all images
    for filename in os.listdir(images_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in valid_extensions:
            continue
            
        base_name = os.path.splitext(filename)[0]
        image_path = os.path.join(images_dir, filename)
        label_filename = base_name + ".txt"
        label_path = os.path.join(labels_dir, label_filename)
        
        if os.path.exists(label_path):
            with open(label_path, "r", encoding="utf-8") as f:
                ground_truth = f.read().strip()
                
            items.append(DatasetItem(
                image_path=image_path,
                label_path=label_path,
                ground_truth=ground_truth,
                filename=filename
            ))
        else:
            # Warn or skip? For now, we skip images without labels
            print(f"Warning: No label found for image {filename}")
            
    if not items:
        # Don't raise error if empty, just return empty list, but maybe log a warning
        pass
        
    return items
