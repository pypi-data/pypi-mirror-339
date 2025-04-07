from typing import List, Literal, Optional
from enum import StrEnum
from pydantic import BaseModel, ConfigDict
import backoff
import logging

logger = logging.getLogger(__name__)


class MessageRole(StrEnum):
    system: str = "system"
    user: str = "user"
    assistant: str = "assistant"
    tool: str = "tool"


class Message(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)
    role: MessageRole = MessageRole.user
    content: str | dict


class LLMClient:
    llm_class = None
    backoff_exceptions = (Exception,)
    backoff_max_retries = 3
    default_format: str = ""

    def __init__(
        self,
        model: str,
        timeout: int = 30,
        system_prompt: str = "",
        chat_messages_limit: Optional[int] = None,
        **client_kwargs,
    ):
        if not self.llm_class:
            raise ValueError("llm_class must be set")
        self.model = model
        self.client = self.get_client(timeout, **client_kwargs)
        self.chat_messages_limit = chat_messages_limit
        self.set_system_prompt(system_prompt)

    def get_client(self, timeout, **kwargs):
        return self.llm_class(timeout=timeout, **kwargs)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            return getattr(self.client, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def call_llm(self, message: str, format: Literal["", "json"] = "", *args, **kwargs):
        raise NotImplementedError
    

    def handle_llm_response(self, response) -> str:
        return response

    def handle_chat_llm_response(self, response) -> Message:
        return Message(content=response, role=MessageRole.assistant)

    @staticmethod
    def _llm_backoff(f):
        def wrapper(*args, **kwargs):
            _class = args[0]
            backoff_wrapper = backoff.on_exception(
                backoff.expo,
                _class.backoff_exceptions,
                max_tries=_class.backoff_max_retries,
            )(f)
            return backoff_wrapper(*args, **kwargs)
        return wrapper

    @_llm_backoff
    def get_message(self, message: str, format: Optional[str] = None, **kwargs):
        if format is None:
            format = self.default_format
        logger.debug(
            "Generate response, model: %s, prompt: %s, system_prompt: %s",
            self.model,
            message,
            self._system_prompt,
        )
        response = self.call_llm(message=message, format=format, **kwargs)
        return self.handle_llm_response(response)

    @_llm_backoff
    def get_chat_message(self, message: str, format: Optional[str] = None, **kwargs):
        if format is None:
            format = self.default_format
        self.history.append(Message(role=MessageRole.user, content=message))
        response = self.call_chat_llm(self.history, format=format)
        parsed_response = self.handle_chat_llm_response(response)
        self.add_history_message(parsed_response)
        return parsed_response

    def set_system_prompt(self, prompt: str) -> None:
        self._system_prompt = prompt
        self.clear_chat_history()

    def get_system_prompt(self) -> str:
        return self._system_prompt

    def get_chat_history(self) -> List[Message]:
        return self.history

    def clear_chat_history(self) -> None:
        self.history = [Message(role=MessageRole.system, content=self._system_prompt)]
