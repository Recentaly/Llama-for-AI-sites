import requests
import logging
import json
import queue
import threading

# this function allows us to translate a message list to a string body
from modules.transform.messages import msg_str

# Setting up basic logging configuration
logging.basicConfig()
logger = logging.getLogger()

class APIClient:
    BASE_URL = "https://www.llama2.ai"
    GENERATE_URL = BASE_URL + "/api"

    def __init__(self, proxy=None):
        # Initialize an HTTP session for making requests
        self.session = requests.Session()
        
        # Define default headers for the session
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Linux; U; Linux x86_64; en-US) Gecko/20100101 Firefox/45.3",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.llama2.ai/",
            "Content-Type": "text/plain;charset=UTF-8",
            "TE": "trailers",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        # Update the session's headers with the default headers
        self.session.headers.update(self.default_headers)

        self.proxy = proxy

    def make_streamed_request(self, *args, **kwargs):
        # Queue to hold response chunks from streaming
        response_chunks_queue = queue.Queue()
        error = None

        def handle_request():
            nonlocal error
            try:
                # Make a POST request with streaming enabled
                response = self.session.post(*args, **kwargs, stream=True)
                
                # Collect and place response chunks into the queue
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:

                        response_chunks_queue.put(chunk)

                # Check for any HTTP errors in the response
                response.raise_for_status()
            except Exception as e:
                error = e

            # Signal the end of chunks in the queue
            response_chunks_queue.put(None)

        # Thread to handle the request
        request_thread = threading.Thread(target=handle_request, daemon=True)
        request_thread.start()

        while True:
            chunk = response_chunks_queue.get()
            if chunk is None:
                break

            yield chunk

    async def generate_text(self, prompt, model, system_prompt: str = "You're an AI assistant", temperature: int = 0.7, top_p: int = 1, max_tokens: int = 600, stream: bool = True, image=None, audio=None):
        # Log the prompt being sent
        logger.info(f"Sending prompt: {prompt}")

        # Initialize output text
        output_text = ""

        # Payload for the request
        payload = {
            "prompt": await msg_str(prompt), # convert prompt to messages list
            "version": model,
            "systemPrompt": system_prompt,
            "temperature": temperature,
            "topP": top_p,
            "maxTokens": max_tokens,
            "image": image,
            "audio": audio
        }
        # Retrieve custom headers for the request
        headers = self.default_headers
        logger.info("Waiting for response")

        if stream:
            # Make a streaming request and process response chunks
            for chunk in self.make_streamed_request(self.GENERATE_URL, headers=headers, data=json.dumps(payload)):

                output_text += await chunk.decode()
                yield chunk.decode()
        else:
            # Make a standard POST request
            response = self.session.post(self.GENERATE_URL, headers=headers, data=json.dumps(payload))

            output_text = response.text
            yield output_text
