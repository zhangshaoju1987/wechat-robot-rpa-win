import ollama
#from ollama import chat
from ollama import ChatResponse
    
class GPT_OLLAMA:
    def __init__(self):
        pass

    def talk(self, prompt, model="deepseek-v2:latest"):

        client = ollama.Client(host='http://ollama.joemeet.com')
        response: ChatResponse = client.chat(model, messages=[
            {"role": "system", "content": "你是一个善解人意且学识渊博的好朋友"},
            {'role': 'user','content': prompt},
        ])
        return response.message.content