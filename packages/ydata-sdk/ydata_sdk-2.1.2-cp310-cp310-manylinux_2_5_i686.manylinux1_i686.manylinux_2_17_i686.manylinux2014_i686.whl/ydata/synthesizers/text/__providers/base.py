"""
    Base class for providers API calls
"""
from enum import Enum
from typing import Any, Optional, Union
from abc import ABC, abstractmethod

from itertools import chain

import pyarrow as pa

class LLMProvider(Enum):
    """Enum for supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

# Output token estimate by response type
response_lengths = {
    "short": 50,
    "medium": 150,
    "long": 500,
    "very_long": 1000
}

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        chat_prompt_template: Optional[str] = None,
    ):
        self.system_prompt = system_prompt
        self.chat_prompt_template = chat_prompt_template

    @abstractmethod
    def get_max_context_length(self, max_new_tokens: int) -> int:
        pass

    @abstractmethod
    def _generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> str:
        """Generate raw text from a final formatted steps."""
        pass

    import pyarrow as pa
    from typing import Optional, Any, List
    from pyarrow import Table

    def generate(
        self,
        table: pa.Table,
        prompt_column: str = "prompt",
        in_context_examples: Optional[list[str]] = None,
        end_instruction: Optional[str] = None,
        sep: str = "\n",
        min_in_context_examples: Optional[int] = None,
        max_in_context_examples: Optional[int] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        return_table: bool = False,
        **kwargs: Any,
    ) -> Union[List[str], pa.Table]:
        """
        Main user-facing generation method. Handles steps formatting and generation.
        Takes a pyarrow.Table as input and applies batch generation based on a specified column.
        """

        if prompt_column not in table.column_names:
            raise ValueError(f"'{prompt_column}' column not found in input table.")

        prompts = []
        for row in table.to_pydict()[prompt_column]:
            # Step 1: Format steps
            prompt = self._format_prompt(
                beg_instruction=row,
                in_context_examples=in_context_examples,
                end_instruction=end_instruction,
                sep=sep,
                min_in_context_examples=min_in_context_examples,
                max_in_context_examples=max_in_context_examples,
            )

            # Step 2: Apply chat template if defined
            final_prompt = self._apply_chat_template(prompt)
            prompts.append(final_prompt)

        # Step 3: Generate responses in batch
        responses = self.generate_batch(
            prompts=prompts,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

        # Step 4: Optionally return a new pyarrow table with the responses added
        if return_table:
            return table.append_column("generated_output", pa.array(responses))

        return responses

    def _format_prompt(
        self,
        beg_instruction: Optional[str],
        in_context_examples: Optional[list[str]],
        end_instruction: Optional[str],
        sep: str,
        min_in_context_examples: Optional[int],
        max_in_context_examples: Optional[int],
    ) -> str:
        in_context_examples = in_context_examples or []

        if len(in_context_examples) > 0:
            if min_in_context_examples is None:
                min_in_context_examples = 1
            if max_in_context_examples is None:
                max_in_context_examples = len(in_context_examples)

            assert min_in_context_examples >= 0
            assert max_in_context_examples >= min_in_context_examples
            assert len(in_context_examples) >= min_in_context_examples

        selected_examples = in_context_examples[:max_in_context_examples] \
            if max_in_context_examples is not None else in_context_examples

        if (
            min_in_context_examples is not None and
            len(selected_examples) < min_in_context_examples
        ):
            raise ValueError(
                f"Cannot fit the minimum {min_in_context_examples} in-context examples."
            )

        parts = list(chain(
            [beg_instruction] if beg_instruction else [],
            selected_examples,
            [end_instruction] if end_instruction else []
        ))

        return sep.join(parts)

    def _apply_chat_template(self, prompt: str) -> str:
        if not self.chat_prompt_template:
            return prompt
        return (
            self.chat_prompt_template
            .replace("{{system_prompt}}", self.system_prompt or "")
            .replace("{{steps}}", prompt)
        )

    def unload_model(self):
        pass
