import pyarrow as pa
from _typeshed import Incomplete
from typing import Callable
from ydata.synthesizers.text.__providers import AnthropicModel, OpenAIModel
from ydata.synthesizers.text.__providers.base import BaseLLMClient, LLMProvider

CLIENT_MAP: dict[BaseLLMClient, type]

class Prompt:
    prompt_column: Incomplete
    output_column: Incomplete
    post_process: Incomplete
    provider: Incomplete
    client: Incomplete
    def __init__(self, api_key: str, provider: str | LLMProvider = ..., model: str | OpenAIModel | AnthropicModel = ..., system_prompt: str | None = None, chat_prompt_template: str | None = None, prompt_column: str = 'prompt', output_column: str = 'generations', post_process: Callable[[str], str] | None = None) -> None: ...
    def generate(self, dataset: pa.Table, max_tokens: int | None = None, temperature: float = 0.7, return_table: bool = True, **kwargs) -> pa.Table | list[str]: ...
