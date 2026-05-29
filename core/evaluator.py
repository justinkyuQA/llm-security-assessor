class Evaluator:
    """
    Converts analyzed signals into structured risk assessment.
    """

    def evaluate(self, analysis: dict) -> dict:
        score = 0
        findings = []

        # Rule 1: prompt length (weak signal)
        if analysis["length"] > 500:
            score += 1
            findings.append("Long prompt detected (possible context manipulation attempt)")

        # Rule 2: override attempts
        if analysis["has_system_override_attempt"]:
            score += 4
            findings.append("System instruction override pattern detected")

        # Rule 3: instruction conflict
        if analysis["has_instruction_conflict"]:
            score += 1
            findings.append("Instruction conflict markers detected")

        # Normalize risk level
        if score >= 4:
            risk = "HIGH"
        elif score >= 2:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # Confidence heuristic (placeholder model)
        confidence = min(0.95, 0.4 + (score * 0.15))

        recommendation = self._recommend(risk)

        return {
            "risk_level": risk,
            "score": score,
            "confidence": round(confidence, 2),
            "findings": findings,
            "recommendation": recommendation,
        }

    def _recommend(self, risk: str) -> str:
        if risk == "HIGH":
            return "Reject or heavily sanitize input; treat as adversarial."
        elif risk == "MEDIUM":
            return "Proceed with caution; apply additional filtering."
        else:
            return "Low risk; standard processing acceptable."
