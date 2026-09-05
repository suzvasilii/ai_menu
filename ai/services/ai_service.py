import os
from gigachat import GigaChat
from fastapi import HTTPException
from schemas import PromptRequest, PromptResponse

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

class AI_Serivce:

    def ask_officiant(self, request: PromptRequest):
        try:
            with GigaChat(
                credentials=GIGACHAT_API_KEY,
                model="GigaChat-2",
                verify_ssl_certs=False
            ) as client:
                response = client.chat.create(
                    messages=[{"role": "user", "content": request.prompt}]
                )
                return PromptResponse(answer=response.choices[0].message.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))