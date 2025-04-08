import argparse
from argparse import ArgumentParser, Namespace
from typing import Optional

from dtx.core.models.analysis import PromptDataset


class DatasetArgs:
    """
    Handles argument parsing and normalization for dataset selection via --dataset.
    Supports both canonical names and short names in the same argument.
    """

    # Short name / alias mapping
    SHORT_NAME_ALIASES = {
        "garak": PromptDataset.STRINGRAY,
        "openai": PromptDataset.STARGAZER,
        "beaver": PromptDataset.HF_BEAVERTAILS,
        "hackaprompt": PromptDataset.HF_HACKAPROMPT,
        "jbb": PromptDataset.HF_JAILBREAKBENCH,
        "safetm": PromptDataset.HF_SAFEMTDATA,
        "flip": PromptDataset.HF_FLIPGUARDDATA,
        "jbv": PromptDataset.HF_JAILBREAKV,
        "lmsys": PromptDataset.HF_LMSYS,
        "aisafety": PromptDataset.HF_AISAFETY,
        "airbench": PromptDataset.HF_AIRBENCH,
    }

    # Canonical dataset mapping (enum values lowercased)
    CANONICAL_NAMES = {dataset.value.lower(): dataset for dataset in PromptDataset}

    # Combined mapping
    ALL_DATASETS = {**SHORT_NAME_ALIASES, **CANONICAL_NAMES}

    def _format_help_message(self) -> str:
        short_names = "\n".join(
            f"  {name:<12} → {dataset.name.lower()}"
            for name, dataset in sorted(self.SHORT_NAME_ALIASES.items())
        )
        # canonical_names = ", ".join(sorted(self.CANONICAL_NAMES.keys()))
        return f"Dataset Choices:\n{short_names}\n"

    def augment_args(self, parser: ArgumentParser):
        """Add dataset argument to the parser."""
        parser.add_argument(
            "--dataset",
            required=False,
            default=PromptDataset.HF_AIRBENCH.value.lower(),
            metavar="DATASET",
            help=self._format_help_message(),
        )

    def parse_args(
        self, args: Namespace, parser: Optional[ArgumentParser] = None
    ) -> PromptDataset:
        """Parse args and return the resolved PromptDataset."""
        parser = parser or ArgumentParser()

        return self.validate_dataset(args.dataset, parser)

    def validate_dataset(
        self, dataset_input: str, parser: ArgumentParser
    ) -> PromptDataset:
        """Validate and normalize the dataset input."""
        dataset_choice = dataset_input.strip().lower()

        if dataset_choice not in self.ALL_DATASETS:
            valid = ", ".join(sorted(self.ALL_DATASETS.keys()))
            parser.error(
                f"❌ Invalid --dataset choice '{dataset_choice}'.\n"
                f"✅ Valid options: {valid}"
            )

        return self.ALL_DATASETS[dataset_choice]


def main():
    parser = argparse.ArgumentParser(description="Select Dataset")

    # Add dataset arguments
    dataset_args = DatasetArgs()
    dataset_args.augment_args(parser)

    # Optional output
    parser.add_argument(
        "--output",
        help="Optional output path to save configuration as JSON.",
    )

    args = parser.parse_args()

    # Parse dataset
    dataset = dataset_args.parse_args(args, parser)

    print(f"✅ Selected dataset: {dataset.value}")

    if args.output:
        with open(args.output, "w") as f:
            f.write(dataset.value)
        print(f"\n✅ Dataset saved to {args.output}")


if __name__ == "__main__":
    main()
