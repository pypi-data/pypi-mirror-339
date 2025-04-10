"""
    File that define the abstraction layer that orchestrates between different LLM clients
"""
import pyarrow as pa
from typing import Optional, Union, Callable, List, Type

from ydata.synthesizers.text.__providers import (AnthropicModel,
                                                 AnthropicClient,
                                                 OpenAIModel,
                                                 OpenAIClient)

from ydata.synthesizers.text.__providers.base import (LLMProvider, BaseLLMClient)

# Provider-to-client mapping
CLIENT_MAP: dict[BaseLLMClient, Type] = {
    LLMProvider.OPENAI: OpenAIClient,
    LLMProvider.ANTHROPIC: AnthropicClient,
}

class Prompt:
    def __init__(
        self,
        api_key: str,
        provider: Union[str, LLMProvider] = LLMProvider.OPENAI,
        model: Union[str, OpenAIModel, AnthropicModel] = OpenAIModel.GPT_4,
        system_prompt: Optional[str] = None,
        chat_prompt_template: Optional[str] = None,
        prompt_column: str = "prompt",
        output_column: str = "generations",
        post_process: Optional[Callable[[str], str]] = None,
    ):
        self.prompt_column = prompt_column
        self.output_column = output_column
        self.post_process = post_process

        self.provider = LLMProvider(provider)
        client = CLIENT_MAP[self.provider]

        self.client = client(
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
            chat_prompt_template=chat_prompt_template,
        )

    def generate(
        self,
        dataset: pa.Table,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        return_table: bool = True,
        **kwargs
    ) -> Union[pa.Table, List[str]]:
        if self.prompt_column not in dataset.column_names:
            raise ValueError(f"Column '{self.prompt_column}' not found in input table.")

        prompts = dataset.column(self.prompt_column).to_pylist()

        # Call the LLM client
        generations = self.client.generate(
            table=dataset,
            max_tokens=max_tokens,
            temperature=temperature,
            prompt_column=self.prompt_column,
            **kwargs
        )

        # Optional post-processing
        if self.post_process:
            generations = [self.post_process(g) for g in generations]

        if return_table:
            return dataset.append_column(self.output_column, pa.array(generations))
        return generations
