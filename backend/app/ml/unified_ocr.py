from typing import Dict, Any, Optional, List
import os

from backend.app.ml.routing.ocr_router import OCRRouter
from backend.app.ml.transformer.inference_trocr import get_trocr_model
from backend.app.services.ocr_pipeline import OCRPipeline
from backend.app.ml.postprocessing.field_extractor import FieldExtractor
from backend.app.ml.postprocessing.validators import FieldValidator

class UnifiedOCR:
    """
    Unified Interface for OCR Operations.
    Orchestrates the entire flow:
    1. Route (Classify)
    2. Select Engine
    3. Execute OCR with Ensemble Strategy
    4. Post-process (Extract & Validate)
    5. Return standardized result
    """
    
    CONFIDENCE_THRESHOLD = 0.85
    
    def __init__(self):
        self.router = OCRRouter()
        self.trocr = get_trocr_model()
        self.easyocr_pipeline = OCRPipeline() # This wraps EasyOCR/Tesseract
        self.extractor = FieldExtractor()
        self.validator = FieldValidator()
        
    def _run_trocr(self, image_path: str) -> Dict[str, Any]:
        res = self.trocr.predict(image_path)
        if "error" in res:
            return {"text": "", "confidence": 0.0, "error": res["error"]}
        return {"text": res.get("text", ""), "confidence": res.get("confidence", 0.0)}

    def _run_easyocr(self, image_path: str) -> Dict[str, Any]:
        res = self.easyocr_pipeline.process_image(image_path, use_easyocr=True)
        return {"text": res.get("text", ""), "confidence": res.get("confidence", 0.0), "structured": res.get("structured", {})}

    def process(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image using the routed OCR engine with ensemble fallback.
        """
        # 1. Route
        route_info = self.router.route(image_path)
        engine = route_info.get("ocr_engine", "easyocr")
        
        result = {
            "routing_info": route_info,
            "text": "",
            "raw_text": "",
            "confidence_score": 0.0,
            "ensemble_triggered": False,
            "structured_fields": {},
            "validation_status": "none",
            "validation_errors": [],
            "corrections_applied": [],
            "metadata": {
                "engine_used": engine,
                "classifier_confidence": route_info.get("confidence", 0.0),
                "document_type": route_info.get("document_type", "unknown")
            }
        }
        
        # 2. Execute with Ensemble Strategy
        try:
            primary_res = {}
            if engine == "trocr":
                primary_res = self._run_trocr(image_path)
            else:
                primary_res = self._run_easyocr(image_path)
            
            result["text"] = primary_res["text"]
            result["confidence_score"] = primary_res["confidence"]
            
            # Ensemble Trigger
            if result["confidence_score"] < self.CONFIDENCE_THRESHOLD:
                result["ensemble_triggered"] = True
                secondary_engine = "easyocr" if engine == "trocr" else "trocr"
                
                secondary_res = {}
                if secondary_engine == "trocr":
                    secondary_res = self._run_trocr(image_path)
                else:
                    secondary_res = self._run_easyocr(image_path)
                
                if secondary_res["confidence"] > result["confidence_score"]:
                    result["text"] = secondary_res["text"]
                    result["confidence_score"] = secondary_res["confidence"]
                    result["metadata"]["engine_used"] = f"ensemble_{secondary_engine}"
                else:
                    result["metadata"]["engine_used"] = f"ensemble_{engine}"
                    
        except Exception as e:
            result["error"] = str(e)
            # Last resort fallback
            if result["text"] == "":
                fallback_res = self._run_easyocr(image_path)
                result["text"] = fallback_res["text"]
                result["confidence_score"] = fallback_res["confidence"]
                result["metadata"]["engine_used"] = "fallback_easyocr"
                    
        # 3. Post-Process (Extract & Validate)
        if result["text"]:
            result["raw_text"] = result["text"]
            
            # Extract
            extracted = self.extractor.extract(result["text"])
            result["structured_fields"] = extracted
            
            # Validate
            status, errors, corrections = self.validator.validate(result["structured_fields"])
            result["validation_status"] = status
            result["validation_errors"] = errors
            result["corrections_applied"].extend(corrections)
            
            # Standardize for Phase C
            result["financial_summary"] = {
                "invoice_id": extracted.get("invoice_id"),
                "date": extracted.get("invoice_date"),
                "subtotal": extracted.get("subtotal"),
                "tax_amount": extracted.get("tax_amount"),
                "tax_percentage": extracted.get("tax_percentage"),
                "discount": extracted.get("discount"),
                "total": extracted.get("total")
            }
            result["line_items"] = extracted.get("line_items", []) # Future: add line item extraction
            result["validation_report"] = {
                "status": status,
                "errors": errors,
                "corrections": corrections
            }
            
        return result
