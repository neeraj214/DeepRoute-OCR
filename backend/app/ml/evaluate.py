import time
import numpy as np
from typing import Dict, Any, List
from .dataset_loader import load_dataset, DatasetItem
from .metrics import compute_cer, compute_wer
from ..services.ocr_pipeline import process_image

def evaluate_dataset(dataset_dir: str, model_name: str = "easyocr") -> Dict[str, Any]:
    """
    Evaluates the OCR model on the given dataset.
    
    Args:
        dataset_dir: Path to the dataset directory.
        model_name: Name of the model to use (currently only 'easyocr' via pipeline).
        
    Returns:
        Dictionary containing evaluation metrics and details.
    """
    items = load_dataset(dataset_dir)
    if not items:
        return {
            "error": "No valid dataset items found",
            "count": 0
        }
        
    results = []
    total_cer = 0.0
    total_wer = 0.0
    total_time = 0.0
    
    print(f"Starting evaluation on {len(items)} images...")
    
    for item in items:
        # Run OCR
        start_time = time.perf_counter()
        try:
            # We use the existing pipeline. 
            # Note: process_image takes (path, lang_hint). We'll assume default or None for now.
            ocr_result = process_image(item.image_path, lang_hint=None)
            predicted_text = ocr_result["text"]
        except Exception as e:
            print(f"Error processing {item.filename}: {e}")
            predicted_text = ""
            
        processing_time = (time.perf_counter() - start_time) * 1000  # ms
        
        # Compute metrics
        cer = compute_cer(item.ground_truth, predicted_text)
        wer = compute_wer(item.ground_truth, predicted_text)
        
        total_cer += cer
        total_wer += wer
        total_time += processing_time
        
        results.append({
            "filename": item.filename,
            "ground_truth": item.ground_truth,
            "predicted": predicted_text,
            "cer": cer,
            "wer": wer,
            "processing_time_ms": processing_time
        })
        
    count = len(items)
    avg_cer = total_cer / count if count > 0 else 0.0
    avg_wer = total_wer / count if count > 0 else 0.0
    avg_time = total_time / count if count > 0 else 0.0
    
    return {
        "model": model_name,
        "dataset_size": count,
        "metrics": {
            "avg_cer": avg_cer,
            "avg_wer": avg_wer,
            "avg_time_ms": avg_time
        },
        "details": results
    }
