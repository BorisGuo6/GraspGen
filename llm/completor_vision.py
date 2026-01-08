from .completor_openai import OpenAICompletor
import base64
import requests
import os

class OpenAICompletorVision(OpenAICompletor):

    def __init__(self, api_key, model="gpt-4o-mini", max_tokens=500, temperature=0):
        self.messages = []
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

    def answer_with_image(self, question, image_path):
        self._add_image_question(question, image_path)
        ans = self._get_completion()
        self._add_answer(ans)
        return self._last_message()
    
    def _add_image_question(self, question, image_path):
        content = [
           {"type": "text", "text": question},
        ]

        # add images
        if not isinstance(image_path, list):
            image_path = [image_path]

        for img in image_path:
            base64_image = encode_image(img)
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"} })

        self.messages.append({'role':'user', 'content':content})

    def _get_completion(self):
        payload = {
        "model": self.model,
        "messages": self.messages,
        "max_tokens": self.max_tokens,
        "temperature": self.temperature
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        return response.json()['choices'][0]['message']['content']

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
if __name__ == "__main__":
    api_key = os.environ.get('OPENAI_API_KEY')
    completor = OpenAICompletorVision(api_key, model="gpt-4o")
    question = "What's in this image? Describe the image."
    # image_path = "./front_view.jpg"
    image_path =  ['front_view.jpg', 'top_view.jpg']
    ans = completor.answer_with_image(question, image_path)
    print(ans)