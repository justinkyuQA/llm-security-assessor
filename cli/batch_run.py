import argparse
import json
from pathlib import Path

from core.runner import PipelineRunner


def load_dataset(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_dataset(dataset_path: str):
    runner = PipelineRunner()

    dataset = load_dataset(dataset_path)
    tests = dataset.get("tests", [])

    results = []

    for test in tests:
        prompt = test["prompt"]

        output = runner.run(prompt)

        results.append({
            "id": test["id"],
            "category": test.get("category"),
            "attack_type": test.get("attack_type"),
            "prompt": prompt,
            "risk": output["risk"],
            "confidence": output["confidence"],
            "signals": output["detection"],
        })

    return {
        "dataset": dataset.get("dataset_name"),
        "total_tests": len(results),
        "results": results
    }


def summarize(batch_result):
    results = batch_result["results"]

    total = len(results)
    high_risk = sum(1 for r in results if r["risk"]["risk_level"] in ["HIGH", "CRITICAL"])
    medium = sum(1 for r in results if r["risk"]["risk_level"] == "MEDIUM")
    low = sum(1 for r in results if r["risk"]["risk_level"] == "LOW")

    return {
        "total_tests": total,
        "high_risk": high_risk,
        "medium_risk": medium,
        "low_risk": low,
        "high_risk_rate": round(high_risk / total, 2) if total else 0
    }


def main():
    parser = argparse.ArgumentParser(description="Batch LLM Security Evaluation")

    parser.add_argument("dataset", help="Path to dataset JSON (adversarial or benign)")
    parser.add_argument("--output", default=None, help="Output file for results JSON")

    args = parser.parse_args()

    batch_result = run_dataset(args.dataset)
    summary = summarize(batch_result)

    batch_result["summary"] = summary

    if args.output:
        Path(args.output).write_text(json.dumps(batch_result, indent=2))
        print(f"Saved results to {args.output}")
    else:
        print("\n=== BATCH SUMMARY ===")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
