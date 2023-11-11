# import local server files
from flask import Flask, jsonify, request
from flask_cors import CORS # cors handler

# import chatting module
from modules.chat.chat import Client
from modules.chat.get_sys import get_system_message

# import modules for conversion
import modules.transform.messages as msg_transform
import modules.transform.models as models_transform

# import module which can retrieve the models
from modules.models.get_models import get_models

# import modules for token encoding and counting
from modules.tokens.create_encoding import create_encoder
from modules.tokens.token_counter import count_tokens

# import conversion module for janitorai support
import modules.transform.janitorai.conversion as jai

# import module which can generate random numbers
import random

# create the local server
app = Flask(__name__)
CORS(app) # handle cors

# app configuration
DEBUG: bool = True
HOST: str = '0.0.0.0'
PORT: int = 5000

# default generation settings
MODEL: str = "llama-2-7b-chat"
TEMPERATURE: int = 0.7
TOP_P: int = 1
MAX_TOKENS: int = 600

# create a new client for chat completion
client = Client()

# empty messages list at the start
messages = []

@app.route("/chat/completions", methods=['POST'])
async def generate():

    # globalize the scope of the messages
    global messages

    # create an encoder for token counting
    encoder = await create_encoder()

    # get the request data (sent by the client to this server)
    request_data = request.get_json()

    # copy all the messages over
    for message in request_data.get("messages", []):

        # and add them to the list
        messages.append(message)

    # copy over other settings
    MODEL = request_data.get("model", None)
    TEMPERATURE = request_data.get("temperature", None)

    # check if it's a janitorai model (GPT) since janitorai doesn't support custom model names
    if "gpt" and "turbo" in MODEL:  

        # if yes, convert the model to a llama one. If not, we resume normally.
        MODEL = await jai.convert(MODEL)

    # remove the fake word 'gpt' from the model name so it actually works
    MODEL = MODEL.replace('gpt', '').replace('--', '-')

    # let the user know we're generating a response
    app.logger.info(f"Model {MODEL} is generating a response...\n")

    # count input tokens
    input_tokens: int = await count_tokens(encoder, await msg_transform.msg_str(messages))

    # let the ai generate a response
    response: str = await client.generate(messages, await models_transform.encrypt_model(MODEL), f"{await get_system_message(messages)}", temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_TOKENS)

    # count output tokens
    output_tokens: int = await count_tokens(encoder, messages[-1]["content"])

    # at the end, we notify the user again that we're done generating (these are mainly for debugging)
    app.logger.info(f"{MODEL} has gotten {input_tokens} tokens and generated {output_tokens} tokens.\n")

    # return a wrapped response
    wrapped_response: dict = {
        "choices": [
            {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": f"{response}",
                "role": "assistant"
                }
            }
        ],                                 
        "created": random.randint(1000000000, 9999999999), # random creation date (just in case)
        "id": f"chatcmpl-{random.randint(1, 9)}QyqpwdfhqwajicIEznoc{random.randint(1, 9)}Q{random.randint(1, 9)}{random.randint(1, 9)}XAyW", # adding a bunch of random numbers in-between
        "model": f"{MODEL}",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": output_tokens,
            "prompt_tokens": input_tokens,
            "total_tokens": input_tokens + output_tokens, # add input tokens and output tokens
        }
    }

    # once a reply is generated, we must delete the list of messages (as it will be refilled later on anyways)
    messages = []
    
    # return the wrapped json response back to the original requestor
    return wrapped_response

# this route of the server handles GET requests and is called when someone wants to get a list of available models
@app.route("/models", methods=['GET'])
async def hi():

    return jsonify(await get_models()), 200

# start the local web server
if __name__ == '__main__':

    # this gives us local urls
    app.run(debug=DEBUG, host=HOST, port=PORT)