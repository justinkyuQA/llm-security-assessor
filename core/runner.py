from core.analyzer import PromptAnalyzer
from core.evaluator import Evaluator


analyzer = PromptAnalyzer()
evaluator = Evaluator()


def run_assessment(prompt: str) -> dict:
    """
    Main pipeline:
    Prompt → Analysis → Evaluation → Report
    """

    analysis = analyzer.analyze(prompt)
    evaluation = evaluator.evaluate(analysis)

    # Final unified report
    return {
        "analysis": analysis,
        **evaluation,
    }
