from ollama import chat
from ollama import ChatResponse

if __name__ == '__main__':
    response: ChatResponse = chat("deepseek-v2:latest", messages=[
            {"role": "system", "content": "你是一个善解人意且学识渊博的好朋友"},
            {'role': 'user','content': "天空为什么是蓝色的？"},
        ])
    print(response["message"]["content"])