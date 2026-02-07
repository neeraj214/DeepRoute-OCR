import pytest
from unittest.mock import MagicMock, patch
from backend.app.ml.routing.ocr_router import OCRRouter

class TestOCRRouter:
    
    @patch('backend.app.ml.routing.ocr_router.os.path.exists')
    @patch('backend.app.ml.routing.ocr_router.get_classifier')
    def test_routing_logic(self, mock_get_classifier, mock_exists):
        """Test if router selects correct engine based on doc type."""
        # Setup mock classifier
        mock_classifier = MagicMock()
        mock_get_classifier.return_value = mock_classifier
        mock_exists.return_value = True
        
        router = OCRRouter()
        
        # Test Case 1: Invoice -> TrOCR
        mock_classifier.predict.return_value = {"document_type": "invoice", "confidence": 0.9}
        result = router.route("dummy_path.jpg")
        assert result["ocr_engine"] == "trocr"
        assert result["document_type"] == "invoice"
        
        # Test Case 2: Note -> EasyOCR
        mock_classifier.predict.return_value = {"document_type": "note", "confidence": 0.8}
        result = router.route("dummy_path.jpg")
        assert result["ocr_engine"] == "easyocr"
        
        # Test Case 3: Low Confidence -> EasyOCR Fallback
        mock_classifier.predict.return_value = {"document_type": "invoice", "confidence": 0.3}
        result = router.route("dummy_path.jpg")
        assert result["ocr_engine"] == "easyocr"
        assert "Low confidence" in result["reasoning"]

    @patch('backend.app.ml.routing.ocr_router.os.path.exists')
    def test_missing_file(self, mock_exists):
        mock_exists.return_value = False
        router = OCRRouter()
        result = router.route("nonexistent.jpg")
        assert "error" in result
