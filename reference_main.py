"""
Run with:
uvicorn main:app --port 8000`
"""
from ragbits.chat.api import RagbitsAPI, ChatInterface
from ragbits.chat.interface.types import ChatContext, TextContent, TextResponse
from ragbits.core.prompt import ChatFormat
from ragbits.core.llms import LiteLLM

class SimpleStreamingChat(ChatInterface):
    def __init__(self):
        self.llm = LiteLLM(model_name="gpt-5.2")

    async def chat(self, message: str, history: ChatFormat, context: ChatContext):
        conversation_history = [
            {"role": "system", "content": "Answer everything relatively shortly"},
            *history,
            {"role": "user", "content": message}
        ]
        result = self.llm.generate_streaming(conversation_history)
        async for event in result:
            yield self.create_text_response(event)

api = RagbitsAPI(
    SimpleStreamingChat,
    cors_origins=["http://localhost:8000", "http://127.0.0.1:8000"]
)

app = api.app
