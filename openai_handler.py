import openai
import requests

class OpenAIHandler:
    def __init__(self, api_key,dynamodb_handler):
        self.api_key = api_key
        self.dynamodb_handler = dynamodb_handler
        openai.api_key = self.api_key

    def get_ai_response(self, prompt, user_id, conversation_history,mode_code):
        try:
            self.dynamodb_handler.update_user_usage(user_id, 1, mode_code)
        except Exception as e:
            return str(e)
        data = {
            "model": "gpt-4",
            "messages": [{"role": "system", "content": "あなたはユーザーが選択したジャンルのストーリーを自動で作成する作成者です。"}]
            + conversation_history
            + [{"role": "user", "content": prompt}],
            "max_tokens": 3000,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get a response from OpenAI: {response.text}")

        response_data = response.json()
        print(response_data)
        return response_data['choices'][0]['message']['content'].strip()
