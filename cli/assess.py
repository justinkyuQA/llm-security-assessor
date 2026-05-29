import argparse
import json
from pathlib import Path

# Core modules (we will implement these next)
from core.runner import run_assessment


def load_input(path: str) -> str:
    """
    Loads a prompt from a file if a path is provided.
    Otherwise treats input as raw text.
    """
    file_path = Path(path)

    if file_path.exists() and file_path.is_file():
        return file_path.read_text(encoding="utf-8")

    # fallback: treat as raw prompt string
    return path


def main():
    parser = argparse.ArgumentParser(
        description="LLM Security Assessment CLI"
    )

    parser.add_argument(
        "input",
        help="Prompt text OR path to a file containing prompts"
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for assessment report"
    )

    args = parser.parse_args()

    prompt = load_input(args.input)

    result = run_assessment(prompt)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print("\n=== LLM SECURITY ASSESSMENT REPORT ===\n")
        print(f"Risk Level: {result.get('risk_level')}")
        print(f"Confidence: {result.get('confidence')}")
        print("\nFindings:")
        for f in result.get("findings", []):
            print(f"- {f}")

        print("\nRecommendation:")
        print(result.get("recommendation", "N/A"))

        print("\nRaw Score:")
        print(result.get("score", "N/A"))


if __name__ == "__main__":
    main()
