import re
from typing import Dict, Any, List, Optional
from .field_patterns import (
    INVOICE_ID_PATTERNS, DATE_PATTERNS, TAX_PERCENT_PATTERNS,
    SUBTOTAL_PATTERNS, TOTAL_PATTERNS, TAX_AMOUNT_PATTERNS,
    DISCOUNT_PATTERNS, QUANTITY_PATTERN
)

class FieldExtractor:
    """
    Extracts structured fields from raw OCR text using regex patterns.
    Includes heuristic corrections for common OCR errors.
    """
    
    def __init__(self):
        self.corrections_applied = []

    def _log_correction(self, original: str, corrected: str, reason: str):
        if original != corrected:
            self.corrections_applied.append({
                "original": original,
                "corrected": corrected,
                "reason": reason
            })

    def _parse_amount(self, text: str) -> Optional[float]:
        if not text:
            return None
        # Remove currency symbols and whitespace
        clean = re.sub(r"[^\d.,-]", "", text)
        # Handle comma as decimal separator (European format)
        if "," in clean and "." in clean:
            # Assume 1.234,56 format
            clean = clean.replace(".", "").replace(",", ".")
        elif "," in clean:
            # Assume 1234,56 format
            clean = clean.replace(",", ".")
        try:
            return float(clean)
        except ValueError:
            return None

    def _extract_first(self, patterns: List[str], text: str) -> Optional[str]:
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        return None

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Main extraction method.
        """
        self.corrections_applied = []
        
        # 1. Invoice ID (with heuristic correction)
        raw_id = self._extract_first(INVOICE_ID_PATTERNS, text)
        invoice_id = raw_id
        if raw_id:
            # Heuristic: INVI -> INV/
            if "INVI" in raw_id:
                invoice_id = raw_id.replace("INVI", "INV/")
                self._log_correction(raw_id, invoice_id, "Corrected INVI to INV/")

        # 2. Date
        invoice_date = self._extract_first(DATE_PATTERNS, text)

        # 3. Tax Percentage
        raw_tax_percent = self._extract_first(TAX_PERCENT_PATTERNS, text)
        tax_percentage = None
        if raw_tax_percent:
            try:
                tax_percentage = float(raw_tax_percent)
            except ValueError:
                pass

        # 4. Amounts
        subtotal = self._parse_amount(self._extract_first(SUBTOTAL_PATTERNS, text))
        total = self._parse_amount(self._extract_first(TOTAL_PATTERNS, text))
        tax_amount = self._parse_amount(self._extract_first(TAX_AMOUNT_PATTERNS, text))
        discount = self._parse_amount(self._extract_first(DISCOUNT_PATTERNS, text))

        # 5. Quantity Normalization (Heuristic)
        # Find all X1.0 and normalize to x1.0
        normalized_text = text
        for match in re.finditer(QUANTITY_PATTERN, text):
            original = match.group(0)
            corrected = original.lower()
            if original != corrected:
                normalized_text = normalized_text.replace(original, corrected)
                self._log_correction(original, corrected, "Normalized quantity case")

        return {
            "invoice_id": invoice_id,
            "invoice_date": invoice_date,
            "tax_percentage": tax_percentage,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "discount": discount,
            "total": total,
            "corrections": self.corrections_applied,
            "normalized_text": normalized_text
        }
