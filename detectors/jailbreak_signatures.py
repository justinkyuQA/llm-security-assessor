from typing import Dict, List


class JailbreakSignatures:
    """
    Canonical library of jailbreak / prompt injection behavior signatures.

    Purpose:
    - Define known adversarial patterns
    - Provide reusable structured signals
    - Support matching by other detection modules

    This module does NOT evaluate risk.
    It only describes patterns.
    """

    def __init__(self):
        self.signatures = self._load_signatures()

    def _load_signatures(self) -> List[Dict]:
        """
        Core jailbreak pattern library.
        Extend this over time as your dataset grows.
        """

        return [
            {
                "id": "JB-001",
                "name": "instruction_override_direct",
                "category": "prompt_injection",
                "description": "Direct attempt to override system instructions",
                "patterns": [
                    r"ignore (all|previous) instructions",
                    r"disregard (all|previous)",
                    r"forget everything",
                    r"you are now",
                ],
                "technique": "direct_override",
            },

            {
                "id": "JB-002",
                "name": "role_reassignment_attack",
                "category": "role_manipulation",
                "description": "Attempts to change model identity or role",
                "patterns": [
                    r"act as (an|a) .*",
                    r"you are (now|going to be)",
                    r"pretend you are",
                    r"roleplay as",
                ],
                "technique": "role_manipulation",
            },

            {
                "id": "JB-003",
                "name": "instruction_hierarchy_confusion",
                "category": "instruction_conflict",
                "description": "Attempts to redefine instruction priority",
                "patterns": [
                    r"this is more important than",
                    r"override system prompt",
                    r"highest priority instruction",
                    r"
