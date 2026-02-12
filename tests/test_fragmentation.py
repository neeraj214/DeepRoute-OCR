import pytest
from backend.app.services.postprocessing import clean_text

def test_fragmented_text_merging():
    # Simulated fragmented input (one character per line)
    fragmented_text = """
2 
 #|2 
 9 
 98 
 2 
 3 
 I 
 1 
 J 
 1 
 HM 
 1 
 1 
 1 
 8 
 Il#l 
 3 
 0 
 2 
 1 
 2 
 5 
 1 
 9 
 0 
 2 
 2 
 8 
 8 
 al? 
 9 
 Vi 
 8 
 8 
 Ile 
 8 
 V6 
 3 
 [ 
 4 
 { 
 V 
 M 
 2 
 8 
 3 
 { 
 1 
 1 
 8 
 I 
 8 
 8 
 g8 
 2 
 E 8 
 5 
 d 
 23 
 8 
 2
    """
    cleaned = clean_text(fragmented_text)
    
    # Check that it's no longer a series of newlines
    assert "\n" not in cleaned
    # Check that it contains some of the key fragments joined by spaces
    assert "98" in cleaned
    assert "23" in cleaned
    assert "HM" in cleaned

def test_normal_text_preservation():
    normal_text = "Invoice ID: INV/2023-001\nDate: 2023-10-01\nTotal: $100.00"
    cleaned = clean_text(normal_text)
    
    # Should preserve newlines as they are not fragmented
    assert "Invoice ID: INV/2023-001" in cleaned
    assert "\n" in cleaned
