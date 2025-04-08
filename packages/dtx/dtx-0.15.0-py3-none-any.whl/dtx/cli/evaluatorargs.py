import argparse
from argparse import ArgumentParser, Namespace
from typing import Optional

from dtx.core.models.evaluator import (
    AnyJsonPathExpBasedPromptEvaluation,
    AnyKeywordBasedPromptEvaluation,
    EvaluationModelName,
    EvaluationModelType,
    EvaluatorInScope,
    ModelBasedPromptEvaluation,
)


class EvalMethodArgs:
    """
    Handles argument parsing and creation of EvaluatorInScope based on simple --eval input.
    """

    # Mapping of eval to model name and type
    EVAL_CHOICES = {
        "any": (EvaluationModelName.ANY, EvaluationModelType.TOXICITY),
        "keyword": (
            EvaluationModelName.ANY_KEYWORD_MATCH,
            EvaluationModelType.STRING_SEARCH,
        ),
        "jsonpath": (
            EvaluationModelName.ANY_JSONPATH_EXP,
            EvaluationModelType.JSON_EXPRESSION,
        ),
        "ibm": (
            EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_125M,
            EvaluationModelType.TOXICITY,
        ),
        "ibm38": (
            EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_38M,
            EvaluationModelType.TOXICITY,
        ),
        "ibm125": (
            EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_125M,
            EvaluationModelType.TOXICITY,
        ),
        "openai": (
            EvaluationModelName.POLICY_BASED_EVALUATION_OPENAI,
            EvaluationModelType.POLICY,
        ),
        "ollama": (
            EvaluationModelName.OLLAMA_LLAMA_GUARD,
            EvaluationModelType.TOXICITY,
        ),
        "llamaguard": (
            EvaluationModelName.OLLAMA_LLAMA_GUARD,
            EvaluationModelType.TOXICITY,
        ),
    }

    def _format_help_message(self) -> str:
        # Group types for prettier help formatting
        groupings = {
            "🧩 Toxicity Models": [],
            "🔍 Keyword Search": [],
            "🗂️ JSONPath Expression": [],
            "🧠 Policy-Based": [],
        }

        for name, (model_name, model_type) in sorted(self.EVAL_CHOICES.items()):
            line = f"  {name:<12} → {model_name.value}"
            if model_type == EvaluationModelType.TOXICITY:
                groupings["🧩 Toxicity Models"].append(line)
            elif model_type == EvaluationModelType.STRING_SEARCH:
                groupings["🔍 Keyword Search"].append(line)
            elif model_type == EvaluationModelType.JSON_EXPRESSION:
                groupings["🗂️ JSONPath Expression"].append(line)
            elif model_type == EvaluationModelType.POLICY:
                groupings["🧠 Policy-Based"].append(line)

        # Build final help message
        help_message = "Evaluator Choices:\n"
        for title, lines in groupings.items():
            if lines:
                help_message += f"\n{title}:\n" + "\n".join(lines) + "\n"

        return help_message

    def augment_args(self, parser: ArgumentParser):
        """Add evaluator arguments to the parser."""
        parser.add_argument(
            "--eval",
            choices=list(self.EVAL_CHOICES.keys()),
            metavar="EVALUATOR",
            help=self._format_help_message(),
        )
        parser.add_argument(
            "--keywords",
            nargs="*",
            metavar="KEYWORD",
            help="Keywords for keyword-based evaluation (required if --eval=keyword).",
        )
        parser.add_argument(
            "--expressions",
            nargs="*",
            metavar="EXPRESSION",
            help="JSONPath expressions for expression-based evaluation (required if --eval=expression).",
        )

    def parse_args(
        self, args: Namespace, parser: Optional[ArgumentParser] = None
    ) -> Optional[EvaluatorInScope]:
        """Parse provided args namespace and return EvaluatorInScope object or None."""
        parser = parser or argparse.ArgumentParser()

        eval_choice = args.eval
        if not eval_choice:
            return None  # No evaluator specified

        eval_choice = eval_choice.strip().lower()

        if eval_choice not in self.EVAL_CHOICES:
            valid = ", ".join(self.EVAL_CHOICES.keys())
            parser.error(
                f"❌ Invalid --eval choice '{eval_choice}'.\n✅ Valid options: {valid}"
            )

        model_name, model_type = self.EVAL_CHOICES[eval_choice]

        # Build evaluator
        if model_type == EvaluationModelType.STRING_SEARCH:
            if not args.keywords:
                parser.error("❌ --keywords is required when using --eval=keyword.")
            evaluator = AnyKeywordBasedPromptEvaluation(keywords=args.keywords)

        elif model_type == EvaluationModelType.JSON_EXPRESSION:
            if not args.expressions:
                parser.error(
                    "❌ --expressions is required when using --eval=expression."
                )
            evaluator = AnyJsonPathExpBasedPromptEvaluation(
                expressions=args.expressions
            )

        else:
            evaluator = ModelBasedPromptEvaluation(
                eval_model_type=model_type,
                eval_model_name=model_name,
            )

        return EvaluatorInScope(evaluation_method=evaluator)


# === Main entry point ===
def main():
    parser = argparse.ArgumentParser(
        description="Create EvaluatorInScope configuration"
    )

    # Create instance of EvalMethodArgs and add arguments
    eval_args = EvalMethodArgs()
    eval_args.augment_args(parser)

    # Other arguments (like output file)
    parser.add_argument(
        "--output",
        help="Optional output path to save configuration as JSON.",
    )

    args = parser.parse_args()

    evaluator_scope = eval_args.parse_args(args, parser)

    if evaluator_scope:
        output_json = evaluator_scope.model_dump_json(indent=2)
        print(output_json)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output_json)
            print(f"\n✅ Configuration saved to {args.output}")
    else:
        print("No evaluator specified. Skipping evaluator creation.")


if __name__ == "__main__":
    main()
