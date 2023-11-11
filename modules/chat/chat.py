# import all modules needed
import json
import logging
import requests

# this function allows us to translate a message list to a string body
from modules.transform.messages import msg_str

# create a logger with basic configuration
logging.basicConfig()
logger = logging.getLogger()

class Client:
    base_url = "https://www.llama2.ai"
    generate_url = base_url + "/api"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Host": "www.llama2.ai",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.llama2.ai/",
            "Content-Length": "428",
            "Origin": "https://www.llama2.ai",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Content-Type": "text/plain;charset=UTF-8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        self.session.headers.update(self.headers)

    async def generate(self, messages: list, model: str, system_prompt: str = "You're an AI assistant", temperature: int = 0.9, top_p: int = 1, max_tokens: int = 600, image=None, audio=None):
        
        payload = {
            "prompt": await msg_str(messages),
            "version": model,
            "systemPrompt": system_prompt,
            "temperature": temperature,
            "topP": top_p,
            "maxTokens": max_tokens,
            "image": image,
            "audio": audio
        }

        response = self.session.post(self.generate_url, headers=self.headers, data=json.dumps(payload))

        # check if generation worked (success = code 200)
        if response.status_code == 200:
        
            # append the received response to the list of messages
            messages.append({"role": "assistant", "content": f"{response.text}"})

            # return the generated text
            return response.text
        
        else:
            logger.error(f"Failed with status code {response.status_code}")
            return None
