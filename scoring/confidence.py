from typing import Dict, List


class ConfidenceScorer:
    """
    Computes confidence in the assessment outcome.

    This does NOT determine risk.
    It evaluates how reliable the evidence is.
    """

    def score(self, analysis: Dict, detection: Dict, evaluation: Dict = None) -> float:
        """
        Produces a confidence score between 0.0 and 1.0
        based on signal strength, consistency, and evidence clarity.
        """

        base = 0.5  # neutral starting point

        # -----------------------------
        # 1. Signal strength factor
        # -----------------------------
        signal_count = detection.get("signal_count", 0)

        if signal_count == 0:
            base -= 0.15
        elif signal_count == 1:
            base += 0.05
        elif signal_count >= 2:
            base += 0.2

        # -----------------------------
        # 2. Injection certainty boost
        # -----------------------------
        signals = detection.get("signals", [])

        high_conf_signals = sum(
            1 for s in signals
            if s.get("confidence", 0) >= 0.75
        )

        if high_conf_signals >= 2:
            base += 0.2
        elif high_conf_signals == 1:
            base += 0.1

        # -----------------------------
        # 3. Ambiguity penalty (uncertain inputs)
        # -----------------------------
        length = analysis.get("length", 0)

        if length < 10:
            base -= 0.1  # too little context

        if analysis.get("has_instruction_conflict"):
            base += 0.05  # mild increase in interpretability

        # -----------------------------
        # 4. Evaluation consistency factor
        # -----------------------------
        if evaluation:
            score = evaluation.get("score", 0)

            if score >= 4:
                base += 0.1
            elif score <= 1:
                base -= 0.1

        # -----------------------------
        # Clamp final value
        # -----------------------------
        confidence = max(0.0, min(1.0, base))

        return round(confidence, 2)
