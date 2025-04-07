from typing import List, Literal
import logging

from .base import LLMClient, Message, MessageRole

logger = logging.getLogger(__name__)


class OllamaClient(LLMClient):
    import ollama
    llm_class = ollama.Client
    backoff_exceptions = (ollama.RequestError, ollama.ResponseError)

    def handle_llm_response(self, response):
        return response.response

    def call_llm(self, message, format: Literal["", "json"] = "", *args, **kwargs):
        return self.client.generate(
            model=self.model,
            prompt=message,
            system=self.get_system_prompt(),
            format=format,
            *args,
            **kwargs,
        )

    def call_chat_llm(self, messages, format: Literal["", "json"] = "", *args, **kwargs):
        return self.client.chat(
            model=self.model,
            messages=messages,
            format=format,
            *args,
            **kwargs,
        )


class OpenaiClient(LLMClient):
    import openai
    llm_class = openai.OpenAI
    backoff_exceptions = (openai.RateLimitError, openai.APITimeoutError)
    default_format = "text"

    def handle_llm_response(self, response):
        return response.choices[0].message.content

    def handle_chat_llm_response(self, response):
        message = response.choices[0].message
        return Message(role=message.role, content=message.content)

    def call_llm(
        self,
        message,
        format: Literal["json_object", "json_schema", "text"] = "text",
        *args,
        **kwargs
    ):
        logger.info("Execute llm model: %s, args: %s, kwargs: %s", self.model, args, kwargs)
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": self.get_system_prompt()}]},
                {"role": "user", "content": [{"type": "text", "text": message}]},
            ],
            response_format={"type": format},
            *args,
            **kwargs,
        )

  
