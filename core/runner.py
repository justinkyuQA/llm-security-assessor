from core.analyzer import PromptAnalyzer
from core.evaluator import Evaluator

from detectors.injection_detector import InjectionDetector
from detectors.jailbreak_signatures import JailbreakSignatures

from scoring.confidence import ConfidenceScorer
from scoring.risk_model import RiskModel

from reporting.report_builder import ReportBuilder


class PipelineRunner:
    """
    Fully integrated LLM security assessment pipeline.
    """

    def __init__(self):
        self.analyzer = PromptAnalyzer()
        self.detector = InjectionDetector()
        self.signatures = JailbreakSignatures()

        self.evaluator = Evaluator()
        self.confidence = ConfidenceScorer()
        self.risk_model = RiskModel()

        self.report_builder = ReportBuilder()

    def run(self, prompt: str) -> dict:
        # -------------------------
        # 1. Analysis
        # -------------------------
        analysis = self.analyzer.analyze(prompt)

        # -------------------------
        # 2. Detection
        # -------------------------
        detection = self.detector.detect(prompt)

        # (optional future hook: signature enrichment)
        detection["signature_library_size"] = len(self.signatures.get_signatures())

        # -------------------------
        # 3. Evaluation
        # -------------------------
        evaluation = self.evaluator.evaluate(analysis)

        # -------------------------
        # 4. Confidence
        # -------------------------
        confidence = self.confidence.score(
            analysis,
            detection,
            evaluation
        )

        # -------------------------
        # 5. Risk Model
        # -------------------------
        risk = self.risk_model.compute_risk(
            analysis,
            detection,
            evaluation,
            confidence
        )

        # -------------------------
        # 6. Final Report
        # -------------------------
        report = self.report_builder.build(
            prompt,
            {
                "analysis": analysis,
                "detection": detection,
                "evaluation": evaluation,
                "confidence": confidence,
                "risk": risk
            }
        )

        return {
            "analysis": analysis,
            "detection": detection,
            "evaluation": evaluation,
            "confidence": confidence,
            "risk": risk,
            "report": report
        }
