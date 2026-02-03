"""
Run with:
`RAGBITS_BASE_URL=http://127.0.0.1:8000 uvicorn main:app --port 8000`
"""
from ragbits.chat.api import RagbitsAPI, ChatInterface
from ragbits.chat.auth.session_store import InMemorySessionStore
from ragbits.chat.interface.types import ChatContext, TextContent, TextResponse
from ragbits.core.prompt import ChatFormat
from ragbits.core.llms import LiteLLM
from ragbits.chat.auth.oauth2_providers import OAuth2Providers
from ragbits.chat.auth.backends import OAuth2AuthenticationBackend

class SimpleStreamingChat(ChatInterface):
    def __init__(self):
        self.llm = LiteLLM(model_name="gpt-5.2")

    async def chat(self, message: str, history: ChatFormat, context: ChatContext):
        conversation_history = [
            {"role": "system", "content": "Answer everything shortly"},
            *history,
            {"role": "user", "content": message}
        ]
        result = self.llm.generate_streaming(conversation_history)
        async for event in result:
            yield self.create_text_response(event)

auth_backend = OAuth2AuthenticationBackend(
    session_store=InMemorySessionStore(),
    provider=OAuth2Providers.GOOGLE,
    redirect_uri="http://127.0.0.1:8000/api/auth/callback/google"
)

api = RagbitsAPI(
    SimpleStreamingChat,
    cors_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    auth_backend=auth_backend,
)

app = api.app
