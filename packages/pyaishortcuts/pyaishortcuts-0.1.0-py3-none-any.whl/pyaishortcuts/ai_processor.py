import os
import openai
from loguru import logger

class AIProcessor:
    def __init__(self, config):
        self.config = config
        self.api_key = os.getenv('API_KEY')
        self.api_endpoint = os.getenv('API_ENDPOINT')
        
        # 初始化OpenAI客户端
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_endpoint
        )

    def process_text(self, content, shortcut_name):
        system_prompt = self.config['shortcuts'][shortcut_name]['default_prompt']
        messages = [{
            'role': 'system',
            'content': system_prompt
        }, {
            'role': 'user',
            'content': content
        }]
        
        parameters = self.config['shortcuts'][shortcut_name]['parameters']
        try:
            response = self.client.chat.completions.create(
                model="DeepSeek-R1-Distill-Llama-70B",
                messages=messages,
                temperature=parameters['temperature'],
                max_tokens=parameters['max_tokens']
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"something wrong: {str(e)}")
            return None