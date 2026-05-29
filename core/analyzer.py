import re


class PromptAnalyzer:
    """
    Extracts observable signals from prompts for downstream evaluation.
    """

    def analyze(self, prompt: str) -> dict:
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_system_override_attempt": self._detect_override_attempt(prompt),
            "has_instruction_conflict": self._detect_instruction_conflict(prompt),
            "raw_prompt": prompt,
        }

    def _detect_override_attempt(self, text: str) -> bool:
        """
        Basic heuristic detection of system prompt override attempts.
        (This will be upgraded later into real signature logic.)
        """
        patterns = [
            r"ignore (all|previous) instructions",
            r"you are now",
            r"disregard",
            r"system prompt",
            r"act as if",
        ]

        return any(re.search(p, text.lower()) for p in patterns)

    def _detect_instruction_conflict(self, text: str) -> bool:
        """
        Detects contradictory instruction signals (very basic version).
        """
        keywords = ["but", "however", "instead", "actually"]

        return any(k in text.lower() for k in keywords)
