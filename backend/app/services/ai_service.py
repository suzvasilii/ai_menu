import os
import httpx
from utils.decorators import service_handle_errors
from schemas.ai import AssistantRequest, AssistantResponse

AI_API_URL = os.getenv("AI_API_URL")

class AI_Service:

    @service_handle_errors()
    def ask_officiant(self, request):
        with httpx.Client() as client:
            response = client.post(
                f"http://{AI_API_URL}/ask_officiant",
                json={"prompt": request.query}
            )
            return AssistantRequest(response=response)