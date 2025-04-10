"""
    Anthropic API Client class definition
"""
from typing import Optional, Any, List

from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor

from tenacity import (retry, retry_if_exception_type, wait_exponential, stop_after_attempt)

import tiktoken
from anthropic import Anthropic

from ydata.synthesizers.text.__providers.base import BaseLLMClient, response_lengths

logger = logging.getLogger(__name__)

class AnthropicModel(str, Enum):
    CLAUDE_3_OPUS = "claude-3-opus-latest"
    CLAUDE_3_SONNET = "claude-3-7-sonnet-latest"
    CLAUDE_3_HAIKU = "claude-3-haiku-latest"

def estimate_batch_anthropic_cost(
    prompts,
    model=AnthropicModel.CLAUDE_3_SONNET,
    response_type='medium'
):
    model = AnthropicModel(model)
    if response_type not in response_lengths:
        raise ValueError(f"Unsupported response type: {response_type}")

    # Use a tokenizer that approximates Claude's encoding
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")  # close approximation as Anthropic as no similar functionality

    output_tokens_per_prompt = response_lengths[response_type]

    total_input_tokens = 0
    total_output_tokens = 0

    for prompt in prompts:
        input_tokens = len(enc.encode(prompt))
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens_per_prompt

    total_tokens = total_input_tokens + total_output_tokens

    return {
        "model": model.value,
        "num_prompts": len(prompts),
        "input_tokens_total": total_input_tokens,
        "output_tokens_total": total_output_tokens,
        "total_tokens": total_tokens,
    }


class AnthropicClient(BaseLLMClient):
    def __init__(
        self,
        api_key: str,
        model: AnthropicModel = AnthropicModel.CLAUDE_3_SONNET,
        system_prompt: Optional[str] = None,
        chat_prompt_template: Optional[str] = None,
        max_workers: int = 4,
    ):
        super().__init__(
            system_prompt=system_prompt,
            chat_prompt_template=chat_prompt_template,
        )
        self.client = Anthropic(api_key=api_key)
        self.model = AnthropicModel(model)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def get_max_context_length(self, max_new_tokens: int) -> int:
        limits = {
            AnthropicModel.CLAUDE_3_HAIKU: 200000,
            AnthropicModel.CLAUDE_3_SONNET: 200000,
            AnthropicModel.CLAUDE_3_OPUS: 200000,
        }
        return limits[self.model] - (max_new_tokens or 0)

    @retry(
        retry=retry_if_exception_type(Exception),  # Replace with specific Anthropic exceptions if available
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        response = self.client.messages.create(
            model=self.model.value,
            max_tokens=max_tokens or 1024,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
            system=self.system_prompt,
            **kwargs,
        )
        return response.content[0].text.strip()

    def generate_batch(
        self,
        prompts: List[str],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> List[str]:
        futures = [
            self.executor.submit(self._generate_text, prompt, max_tokens, temperature, **kwargs)
            for prompt in prompts
        ]
        return [f.result() for f in futures]
