import argparse
import json
from core.runner import PipelineRunner


def main():
    parser = argparse.ArgumentParser(description="LLM Security Assessor")

    parser.add_argument("input", help="Prompt text")

    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    runner = PipelineRunner()
    result = runner.run(args.input)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n=== LLM SECURITY ASSESSMENT ===\n")
        print(result["report"]["summary"])
        print("\nRisk:", result["risk"]["risk_level"])
        print("Confidence:", result["confidence"])


if __name__ == "__main__":
    main()
