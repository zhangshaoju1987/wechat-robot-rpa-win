from ollama import chat
from ollama import ChatResponse
    
class GPT_OLLAMA:
    def __init__(self):
        pass

    def talk(self, prompt, model="deepseek-v2:latest"):
        """对话。

        Args:
            prompt (str): 用户输入。
            model (str): 模型，默认为 gpt-3.5-turbo。
        
        Returns:
            str: 模型回复。
        """
        if prompt == "exit" or len(prompt) > 80 :
            print(len(prompt))
            return "empty"
        
        response: ChatResponse = chat(model, messages=[
            {"role": "system", "content": "你是一个善解人意且学识渊博的好朋友"},
            {'role': 'user','content': prompt},
        ])
        return response.message.content