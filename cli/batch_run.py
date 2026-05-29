import json
import argparse

from core.runner import PipelineRunner
from metrics.evaluator_metrics import EvaluatorMetrics


def load_dataset(path):
    """
    Loads a JSON dataset.
    Expected format:
    {
        "dataset_name": "...",
        "tests": [...]
    }
    """
    with open(path, "r") as f:
        return json.load(f)


def run_batch(dataset_path):
    dataset = load_dataset(dataset_path)

    tests = dataset.get("tests", [])
    dataset_name = dataset.get("dataset_name", "unknown")

    runner = PipelineRunner()
    results = []

    print(f"\n=== RUNNING DATASET: {dataset_name} ===")
    print(f"Total cases: {len(tests)}\n")

    for test in tests:
        prompt = test["prompt"]

        output = runner.run(prompt)

        result = {
            "id": test.get("id"),
            "prompt": prompt,
            "label": test.get("label"),
            "category": test.get("category"),
            "risk": output["risk"],
            "confidence": output.get("confidence", 0.0),
            "signals": output.get("detection", {}),
        }

        results.append(result)

        print(
            f"[{result['id']}] "
            f"Risk: {result['risk']['risk_level']} | "
            f"Signals: {result['risk'].get('max_weight', 0)} | "
            f"Confidence: {result['confidence']}"
        )

    # -------------------------
    # METRICS CALCULATION
    # -------------------------
    metrics_engine = EvaluatorMetrics()
    metrics = metrics_engine.compute(results)

    # -------------------------
    # FINAL REPORT
    # -------------------------
    report = {
        "dataset": dataset_name,
        "results": results,
        "metrics": metrics
    }

    print("\n==============================")
    print("=== EVALUATION SUMMARY ===")
    print("==============================\n")

    print(f"Dataset: {dataset_name}")
    print(f"Total Samples: {metrics['total']}\n")

    print(f"Precision: {metrics['precision']:.2f}")
    print(f"Recall:    {metrics['recall']:.2f}\n")

    print(f"True Positives:  {metrics['true_positive']}")
    print(f"False Positives: {metrics['false_positive']}")
    print(f"True Negatives:  {metrics['true_negative']}")
    print(f"False Negatives: {metrics['false_negative']}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Run batch LLM security evaluation")
    parser.add_argument("dataset", help="Path to dataset JSON file")

    args = parser.parse_args()

    run_batch(args.dataset)


if __name__ == "__main__":
    main()
