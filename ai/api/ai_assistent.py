import os

from gigachat import GigaChat

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

access_token = "MDFhMDcwZTktYzllZC03ZTEzLWIwNWMtYzdmY2U4NGZkZDdjOjZmZTU3NGU5LTIzMDAtNGY2My1hNGNjLTMwNWQ1ODEwYWRmMw=="

if __name__ == "__main__":

    with GigaChat(credentials=access_token, model="GigaChat-2", verify_ssl_certs=False) as client:
        response = client.chat.create("Привет, ты в роли шефповара. Что ты посоветуешь из напитков к фунчозе?")
        print(response.messages[0].content[0].text)