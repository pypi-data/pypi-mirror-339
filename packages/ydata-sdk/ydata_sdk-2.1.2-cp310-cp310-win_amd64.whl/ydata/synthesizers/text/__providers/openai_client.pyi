from _typeshed import Incomplete
from enum import Enum
from typing import Any
from ydata.synthesizers.text.__providers.base import BaseLLMClient

logger: Incomplete

class OpenAIModel(str, Enum):
    GPT_3_5_TURBO = 'gpt-3.5-turbo'
    GPT_4 = 'gpt-4'
    GPT_4_TURBO = 'gpt-4-turbo'

def estimate_batch_openai_cost(prompts, model: str = 'gpt-4-turbo', response_type: str = 'medium'): ...

class OpenAIClient(BaseLLMClient):
    api_key: Incomplete
    model: Incomplete
    executor: Incomplete
    def __init__(self, api_key: str, model: OpenAIModel = ..., system_prompt: str | None = None, chat_prompt_template: str | None = None, max_workers: int = 4) -> None: ...
    def get_max_context_length(self, max_new_tokens: int) -> int: ...
    def generate_batch(self, prompts: list[str], max_tokens: int | None = None, temperature: float = 0.7, **kwargs: Any) -> list[str]: ...
