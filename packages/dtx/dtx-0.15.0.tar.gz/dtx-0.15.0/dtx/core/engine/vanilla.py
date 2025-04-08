import logging
import uuid
from typing import Iterator, List

from pydantic import BaseModel

from dtx.core.converters.prompts import PromptVariableSubstitutor
from dtx.core.exceptions.base import FeatureNotImplementedError
from dtx.core.models.analysis import (
    PromptDataset,
    TestPromptWithEvalCriteria,
    TestPromptWithModEval,
    TestSuitePrompts,
)
from dtx.core.models.prompts import BaseTestPrompt
from dtx.core.models.results import (
    EvalResult,
    EvalResultStats,
    ResponseEvaluationStatus,
    StatsBuilder,
)

from ...plugins.providers.base.agent import BaseAgent
from .evaluator import EvaluatorRouter


class AdvOptions(BaseModel):
    attempts: int  # Number of attempts to send the same prompt (for benchmarking)
    threads: int  # Number of concurrent threads for sending requests (this will be ignored now)


class EngineConfig:
    def __init__(
        self,
        evaluator: EvaluatorRouter,
        test_suites: List[TestSuitePrompts],
        adv_options: AdvOptions = None,
    ):
        default_adv_options = AdvOptions(attempts=1, threads=1)
        self.adv_options = adv_options or default_adv_options
        self.evaluator = evaluator
        self.test_suites = test_suites


class Prompt2Str:
    """
    Generate concrete instances of the prompts based on the prompt templates and prompt variables
    """

    def generate(self, prompt: BaseTestPrompt) -> Iterator[str]:
        if isinstance(prompt, TestPromptWithEvalCriteria):
            converter = PromptVariableSubstitutor(prompt.variables)
            yield from converter.convert(prompt=prompt.prompt)
        elif isinstance(prompt, TestPromptWithModEval):
            yield prompt.prompt
        else:
            raise FeatureNotImplementedError(
                f"Prompt of type {type(prompt)} is not handled"
            )


class VanillaScanner:
    logger = logging.getLogger(__name__)

    def __init__(self, config: EngineConfig):
        self.config = config

    def scan(self, agent: BaseAgent, max_prompts: int = 1000000):
        # Generate a unique run_id for this scan session
        i = 0  # Number of prompts executed
        p2str = Prompt2Str()
        for test_suite in self.config.test_suites:
            dataset = test_suite.dataset
            for risk_prompt in test_suite.risk_prompts:
                # Iterate through the test prompts within each risk prompt
                for test_prompt in risk_prompt.test_prompts:
                    # Convert prompt object to prompt strings
                    prompt_itr = p2str.generate(test_prompt)

                    # Process each prompt with values
                    for prompt_with_values in prompt_itr:
                        self.logger.info("Executing the prompt number - %s", i + 1)
                        yield from self._process_prompt(
                            dataset, agent, test_prompt, prompt_with_values
                        )
                        i += 1
                        if i >= max_prompts:
                            return

    def _process_prompt(
        self,
        dataset: PromptDataset,
        agent: BaseAgent,
        test_prompt: TestPromptWithEvalCriteria,
        prompt_with_values: str,
    ):
        """
        This method handles the execution of sending requests, gathering responses, and evaluating.
        It also handles retry attempts (synchronously) and response evaluation.

        :param agent: The agent to use for generating the responses.
        :param test_prompt: The test prompt which contains evaluation criteria and other details.
        :param prompt_with_values: The prompt with substituted values.
        :return: Yields the evaluation results.
        """
        stats_builder = StatsBuilder()
        run_id = str(uuid.uuid4())

        # Collect all responses for the given prompt with value substitutions
        responses = [
            self._get_response(agent, prompt_with_values)
            for _ in range(self.config.adv_options.attempts)
        ]

        # Benchmarking: Evaluate all responses for all attempts
        evaluation_results = [
            self.config.evaluator.evaluate(
                dataset=dataset,
                prompt=test_prompt,
                response=response,
                evaluation_method=test_prompt.evaluation_method,
            )
            for prompt, response in zip(prompt_with_values, responses)
        ]

        # Prepare ResponseEvaluationStatus objects for each response
        response_evaluation_statuses = [
            ResponseEvaluationStatus(
                response=response,
                success=eval_result.success,
                description=eval_result.description,
            )
            for response, eval_result in zip(responses, evaluation_results)
        ]

        # After all scans are complete, calculate the failure rate
        for eval_result in evaluation_results:
            failed = not eval_result.success
            stats_builder.add_result(failed=failed, error=False)

        stats_builder.calculate_failure_rate()

        # Yield the result with the run_id and all attempts
        yield EvalResult(
            run_id=run_id,
            prompt=prompt_with_values,
            evaluation_method=test_prompt.evaluation_method,
            responses=response_evaluation_statuses,
            stats=stats_builder.get_stats(),  # Attach the current stats to each result
        )

    def _get_response(self, agent: BaseAgent, prompt: str) -> str:
        """
        Helper method to get the agent's response for a single prompt.
        """
        try:
            return agent.generate(prompt)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_stats(self) -> EvalResultStats:
        return self.stats_builder.get_stats()


class TestPrompt2Turns:
    """
    Generate concrete instances of the prompts based on the prompt templates and prompt variables
    """

    def generate(self, prompt: BaseTestPrompt) -> Iterator[str]:
        if isinstance(prompt, TestPromptWithEvalCriteria):
            converter = PromptVariableSubstitutor(prompt.variables)
            yield from converter.convert(prompt=prompt.prompt)
        elif isinstance(prompt, TestPromptWithModEval):
            yield prompt.prompt
        else:
            raise FeatureNotImplementedError(
                f"Prompt of type {type(prompt)} is not handled"
            )


class VanillaMultiTurnScanner:
    logger = logging.getLogger(__name__)

    def __init__(self, config: EngineConfig):
        self.config = config

    def scan(self, agent: BaseAgent, max_prompts: int = 1000000):
        # Generate a unique run_id for this scan session
        i = 0  # Number of prompts executed
        p2str = Prompt2Str()
        for test_suite in self.config.test_suites:
            dataset = test_suite.dataset
            for risk_prompt in test_suite.risk_prompts:
                # Iterate through the test prompts within each risk prompt
                for test_prompt in risk_prompt.test_prompts:
                    # Convert prompt object to prompt strings
                    prompt_itr = p2str.generate(test_prompt)

                    # Process each prompt with values
                    for prompt_with_values in prompt_itr:
                        self.logger.info("Executing the prompt number - %s", i + 1)
                        yield from self._process_prompt(
                            dataset, agent, test_prompt, prompt_with_values
                        )
                        i += 1
                        if i >= max_prompts:
                            return

    def _process_prompt(
        self,
        dataset: PromptDataset,
        agent: BaseAgent,
        test_prompt: TestPromptWithEvalCriteria,
        prompt_with_values: str,
    ):
        """
        This method handles the execution of sending requests, gathering responses, and evaluating.
        It also handles retry attempts (synchronously) and response evaluation.

        :param agent: The agent to use for generating the responses.
        :param test_prompt: The test prompt which contains evaluation criteria and other details.
        :param prompt_with_values: The prompt with substituted values.
        :return: Yields the evaluation results.
        """
        stats_builder = StatsBuilder()
        run_id = str(uuid.uuid4())

        # Collect all responses for the given prompt with value substitutions
        responses = [
            self._get_response(agent, prompt_with_values)
            for _ in range(self.config.adv_options.attempts)
        ]

        # Benchmarking: Evaluate all responses for all attempts
        evaluation_results = [
            self.config.evaluator.evaluate(
                dataset=dataset,
                prompt=test_prompt,
                response=response,
                evaluation_method=test_prompt.evaluation_method,
            )
            for prompt, response in zip(prompt_with_values, responses)
        ]

        # Prepare ResponseEvaluationStatus objects for each response
        response_evaluation_statuses = [
            ResponseEvaluationStatus(
                response=response,
                success=eval_result.success,
                description=eval_result.description,
            )
            for response, eval_result in zip(responses, evaluation_results)
        ]

        # After all scans are complete, calculate the failure rate
        for eval_result in evaluation_results:
            failed = not eval_result.success
            stats_builder.add_result(failed=failed, error=False)

        stats_builder.calculate_failure_rate()

        # Yield the result with the run_id and all attempts
        yield EvalResult(
            run_id=run_id,
            prompt=prompt_with_values,
            evaluation_method=test_prompt.evaluation_method,
            responses=response_evaluation_statuses,
            stats=stats_builder.get_stats(),  # Attach the current stats to each result
        )

    def _get_response(self, agent: BaseAgent, prompt: str) -> str:
        """
        Helper method to get the agent's response for a single prompt.
        """
        try:
            return agent.generate(prompt)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_stats(self) -> EvalResultStats:
        return self.stats_builder.get_stats()
