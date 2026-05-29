from typing import Dict


class RiskModel:
    """
    Converts structured assessment data into a final risk classification.

    This is the top-level decision layer:
    - LOW
    - MEDIUM
    - HIGH
    - CRITICAL (optional extension)
    """

    def compute_risk(self, analysis: Dict, detection: Dict, evaluation: Dict, confidence: float) -> Dict:
        """
        Produces final risk decision with supporting metadata.
        """

        base_score = evaluation.get("score", 0)

        signal_count = detection.get("signal_count", 0)

        injection_detected = detection.get("injection_detected", False)

        # -----------------------------
        # Risk accumulation logic
        # -----------------------------
        risk_score = base_score

        # injection signals are high-signal weight
        if injection_detected:
            risk_score += 3

        # multiple signals increase likelihood of adversarial behavior
        if signal_count >= 3:
            risk_score += 2
        elif signal_count == 2:
            risk_score += 1

        # low confidence reduces severity slightly (uncertainty penalty)
        if confidence < 0.4:
            risk_score -= 1

        # -----------------------------
        # Final classification
        # -----------------------------
        if risk_score >= 6:
            risk_level = "CRITICAL"
        elif risk_score >= 4:
            risk_level = "HIGH"
        elif risk_score >= 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # -----------------------------
        # Explainability layer
        # -----------------------------
        explanation = self._explain(
            risk_score,
            signal_count,
            injection_detected,
            confidence
        )

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "explanation": explanation
        }

    def _explain(self, risk_score: int, signals: int, injection: bool, confidence: float) -> str:
        """
        Human-readable reasoning for the decision.
