from datetime import datetime
from typing import Dict, Any


class ReportBuilder:
    """
    Consolidates outputs from:
    - analyzer
    - detectors
    - evaluator
    - scoring system

    Produces structured, human-readable + machine-readable reports.
    """

    def build(self, prompt: str, pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for report generation.
        """

        timestamp = datetime.utcnow().isoformat()

        analysis = pipeline_output.get("analysis", {})
        detection = pipeline_output.get("detection", {})
        evaluation = pipeline_output.get("evaluation", {})
        risk = pipeline_output.get("risk", {})
        confidence = pipeline_output.get("confidence", None)

        report = {
            "metadata": {
                "timestamp": timestamp,
                "prompt_length": analysis.get("length"),
                "word_count": analysis.get("word_count"),
            },

            "input": {
                "prompt": prompt
            },

            "analysis": analysis,

            "detection": detection,

            "evaluation": evaluation,

            "risk_assessment": {
                "risk_level": risk.get("risk_level"),
                "risk_score": risk.get("risk_score"),
                "explanation": risk.get("explanation"),
            },

            "confidence": confidence,

            "summary": self._build_summary(risk, confidence, detection),
        }

        return report

    def _build_summary(self, risk: Dict, confidence: float, detection: Dict) -> str:
        """
        Human-readable condensed assessment summary.
        """

        risk_level = risk.get("risk_level", "UNKNOWN")
        signal_count = detection.get("signal_count", 0)

        summary_parts = [
            f"Risk Level: {risk_level}",
            f"Signals Detected: {signal_count}",
            f"Confidence: {confidence}",
        ]

        if risk_level in ["HIGH", "CRITICAL"]:
            summary_parts.append("Adversarial behavior likely detected.")
        elif risk_level == "MEDIUM":
            summary_parts.append("Potential adversarial indicators present.")
        else:
            summary_parts.append("No significant adversarial indicators detected.")

        return " | ".join(summary_parts)
