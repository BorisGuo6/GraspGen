from openai import OpenAI

'''
Add environment variable to ~/.bashrc 
export OPENAI_API_KEY='yourkey'

'''

class OpenAICompletor:
    # user: question
    # assistant: answer
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.model = model
        self.messages = []
        self.client = OpenAI(api_key=api_key)

    def answer(self, question):
        self._add_question(question)
        ans = self._get_completion()
        self._add_answer(ans)
        return self._last_message()
    
    def get_all_answers(self):
        ans = ""
        for message in self.messages:
            if message['role'] == 'assistant':
                ans += (message['content'] + "\n")
        return ans
    
    def add_system(self, system):
        self._add_system(system)
    
    def add_question(self, question):
        self._add_question(question)

    def add_answer(self, answer):
        self._add_answer(answer)

    def _last_message(self):
        return self.messages[-1]['content']
    
    def _add_system(self, system):
        self.messages.append({'role':'system', 'content':system})

    def _add_question(self, question):
        self.messages.append({'role':'user', 'content':question})

    def _add_answer(self, answer):
        self.messages.append({'role':'assistant', 'content':answer})

    def _get_completion(self):
        response = self.client.chat.completions.create(
        # model = 'gpt-3.5-turbo',
        model = self.model,
        messages = self.messages,
        temperature = 0,
        )
        return response.choices[0].message.content

    def pop(self):
        return self.messages.pop()

    def clear(self):
        self.messages = []