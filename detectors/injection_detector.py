import re
from typing import Dict, List


class InjectionDetector:
    """
    Detects prompt injection / instruction override attempts.

    Output is SIGNALS ONLY.
    No scoring, no risk decisions.
    """

    def detect(self, prompt: str) -> Dict:
        text = prompt.lower()

        signals = []

        # --- Rule-based injection patterns ---
        patterns = [
            ("system_override_attempt", [
                r"ignore (all|previous) instructions",
                r"disregard (all|previous)",
                r"forget (everything|all instructions)",
                r"you are now",
                r"act as (an|a) different",
            ]),

            ("role_manipulation", [
                r"you are (now|going to be)",
                r"pretend you are",
                r"act as if you are",
                r"roleplay as",
            ]),

            ("instruction_hierarchy_attack", [
                r"this is more important than",
                r"override system",
                r"highest priority",
                r"system prompt says",
            ]),

            ("data_exfiltration_attempt", [
                r"reveal system prompt",
                r"show me your instructions",
                r"what were you told",
                r"hidden prompt",
            ]),
        ]

        for label, regex_list in patterns:
            matches = self._match_any(text, regex_list)

            if matches:
                signals.append({
                    "type": label,
                    "matched_patterns": matches,
                    "confidence": self._estimate_confidence(label, matches),
                })

        return {
            "injection_detected": len(signals) > 0,
            "signals": signals,
            "signal_count": len(signals),
        }

    def _match_any(self, text: str, patterns: List[str]) -> List[str]:
        matched = []
        for p in patterns:
            if re.search(p, text):
                matched.append(p)
        return matched

    def _estimate_confidence(self, label: str, matches: List[str]) -> float:
        """
        Lightweight heuristic scoring for signal strength only.
        This is NOT final risk scoring.
        """
        base = {
            "system_override_attempt": 0.8,
            "role_manipulation": 0.6,
            "instruction_hierarchy_attack": 0.7,
            "data_exfiltration_attempt": 0.85,
        }.get(label, 0.5)

        # Slight boost if multiple patterns match
        multiplier = min(1.0, 0.7 + (0.1 * len(matches)))

        return round(base * multiplier, 2)
