from _typeshed import Incomplete
from enum import Enum
from typing import Any
from ydata.synthesizers.text.__providers.base import BaseLLMClient

logger: Incomplete

class AnthropicModel(str, Enum):
    CLAUDE_3_OPUS = 'claude-3-opus-latest'
    CLAUDE_3_SONNET = 'claude-3-7-sonnet-latest'
    CLAUDE_3_HAIKU = 'claude-3-haiku-latest'

def estimate_batch_anthropic_cost(prompts, model=..., response_type: str = 'medium'): ...

class AnthropicClient(BaseLLMClient):
    client: Incomplete
    model: Incomplete
    executor: Incomplete
    def __init__(self, api_key: str, model: AnthropicModel = ..., system_prompt: str | None = None, chat_prompt_template: str | None = None, max_workers: int = 4) -> None: ...
    def get_max_context_length(self, max_new_tokens: int) -> int: ...
    def generate_batch(self, prompts: list[str], max_tokens: int | None = None, temperature: float = 0.7, **kwargs: Any) -> list[str]: ...
