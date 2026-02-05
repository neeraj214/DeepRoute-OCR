import pytest
from backend.app.ml.metrics import compute_cer, compute_wer
from backend.app.ml.dataset_loader import load_dataset
import os

def test_cer_perfect_match():
    assert compute_cer("hello", "hello") == 0.0

def test_cer_substitution():
    # hullo vs hello: 1 sub, len 5 -> 0.2
    assert compute_cer("hello", "hullo") == 0.2

def test_cer_deletion():
    # hell vs hello: 1 del, len 5 -> 0.2
    assert compute_cer("hello", "hell") == 0.2

def test_cer_insertion():
    # helloo vs hello: 1 ins, len 5 -> 0.2
    assert compute_cer("hello", "helloo") == 0.2

def test_wer_perfect_match():
    assert compute_wer("hello world", "hello world") == 0.0

def test_wer_substitution():
    # hello there vs hello world: 1 sub, 2 words -> 0.5
    assert compute_wer("hello world", "hello there") == 0.5

def test_dataset_loader():
    # This test relies on the sample dataset created by scripts/create_sample_dataset.py
    # We assume it has been run or we can mock it.
    # For now, let's create a temporary structure or skip if not present.
    dataset_path = "datasets/ocr_eval"
    if not os.path.exists(dataset_path):
        pytest.skip("Dataset not found")
        
    items = load_dataset(dataset_path)
    assert len(items) > 0
    item = items[0]
    assert os.path.exists(item.image_path)
    assert os.path.exists(item.label_path)
    assert item.ground_truth is not None

