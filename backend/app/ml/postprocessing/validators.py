from typing import Dict, Any, List, Optional, Tuple
import math

class FieldValidator:
    """
    Validates structured fields extracted from OCR.
    Checks math consistency and format compliance.
    """
    
    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance
        self.validation_errors = []
        self.corrections = []

    def _log_error(self, message: str):
        self.validation_errors.append(message)

    def _log_correction(self, field: str, original: Any, corrected: Any, reason: str):
        self.corrections.append({
            "field": field,
            "original": original,
            "corrected": corrected,
            "reason": reason
        })

    def validate(self, fields: Dict[str, Any]) -> Tuple[str, List[str], List[Dict[str, Any]]]:
        """
        Validates fields and returns (status, errors, corrections).
        Status can be 'valid', 'corrected', or 'invalid'.
        """
        self.validation_errors = []
        self.corrections = []
        
        subtotal = fields.get("subtotal")
        tax_amount = fields.get("tax_amount")
        discount = fields.get("discount", 0.0) or 0.0
        total = fields.get("total")
        tax_percent = fields.get("tax_percentage")

        # 1. Basic Existence Checks
        if total is None:
            self._log_error("Missing total amount")
        if subtotal is None:
            self._log_error("Missing subtotal amount")

        # 2. Math Consistency: subtotal + tax - discount == total
        if subtotal is not None and total is not None:
            calculated_tax = tax_amount if tax_amount is not None else 0.0
            expected_total = subtotal + calculated_tax + discount # discount is usually negative in OCR
            
            if not math.isclose(expected_total, total, abs_tol=self.tolerance):
                # Try to see if tax_percent helps explain the gap
                if tax_percent is not None and tax_amount is None:
                    estimated_tax = round(subtotal * (tax_percent / 100.0), 2)
                    expected_total_with_tax = subtotal + estimated_tax + discount
                    
                    if math.isclose(expected_total_with_tax, total, abs_tol=self.tolerance):
                        self._log_correction("tax_amount", None, estimated_tax, f"Inferred from tax_percent ({tax_percent}%)")
                        fields["tax_amount"] = estimated_tax
                    else:
                        self._log_error(f"Math inconsistency: subtotal({subtotal}) + tax({tax_amount}) + discount({discount}) != total({total})")
                else:
                    self._log_error(f"Math inconsistency: subtotal({subtotal}) + tax({tax_amount}) + discount({discount}) != total({total})")

        # 3. Percentage Bounds
        if tax_percent is not None:
            if not (0 <= tax_percent <= 100):
                self._log_error(f"Invalid tax percentage: {tax_percent}")

        # Determine status
        if not self.validation_errors and not self.corrections:
            status = "valid"
        elif not self.validation_errors and self.corrections:
            status = "corrected"
        else:
            status = "invalid"

        return status, self.validation_errors, self.corrections
