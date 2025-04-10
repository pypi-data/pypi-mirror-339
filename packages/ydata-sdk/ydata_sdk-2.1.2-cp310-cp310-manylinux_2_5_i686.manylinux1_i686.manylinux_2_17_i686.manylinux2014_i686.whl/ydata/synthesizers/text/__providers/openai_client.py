"""
    OpenAI API Client class definition
"""
import os
from enum import Enum

from typing import Optional, Any, List
from concurrent.futures import ThreadPoolExecutor
import logging

import tiktoken
import openai


from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from ydata.synthesizers.text.__providers.base import BaseLLMClient, response_lengths
from ydata.synthesizers.text.__providers.base import BaseLLMClient

logger = logging.getLogger(__name__)

class OpenAIModel(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"

def estimate_batch_openai_cost(
    prompts,
    model="gpt-4-turbo",
    response_type="medium"
):
    model = OpenAIModel(model)
    if response_type not in response_lengths:
        raise ValueError(f"Unsupported response type: {response_type}")

    # Load tokenizer for model
    enc = tiktoken.encoding_for_model(model.value)
    output_tokens_per_prompt = response_lengths[response_type]

    total_input_tokens = 0
    total_output_tokens = 0

    for prompt in prompts:
        input_tokens = len(enc.encode(prompt))
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens_per_prompt

    total_tokens = total_input_tokens + total_output_tokens

    return {
        "model": model,
        "num_prompts": len(prompts),
        "input_tokens_total": total_input_tokens,
        "output_tokens_total": total_output_tokens,
        "total_tokens": total_tokens
    }


class OpenAIClient(BaseLLMClient):
    def __init__(
        self,
        api_key: str,
        model: OpenAIModel = OpenAIModel.GPT_3_5_TURBO,
        system_prompt: Optional[str] = None,
        chat_prompt_template: Optional[str] = None,
        max_workers: int = 4,
    ):
        super().__init__(system_prompt=system_prompt, chat_prompt_template=chat_prompt_template)
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def get_max_context_length(self, max_new_tokens: int) -> int:
        limits = {
            OpenAIModel.GPT_3_5_TURBO: 4096,
            OpenAIModel.GPT_4: 8192,
            OpenAIModel.GPT_4_TURBO: 128000,
        }
        return limits[self.model] - (max_new_tokens or 0)

    @retry(
        retry=retry_if_exception_type((openai.RateLimitError, openai.APIError, openai.APIConnectionError)),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> str:
        messages = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = openai.chat.completions.create(
            model=self.model.value,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
        return response.choices[0].message.content.strip()

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
        return [future.result() for future in futures]


