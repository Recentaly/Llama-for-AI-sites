# this file returns a list of supported models with type dict
# example output: {"data": [{"id": "gpt.3-5-turbo"}, {"id": "gpt-4"}]}

# notice the word 'gpt' which is completely out of place? Venus.chub.ai doesn't recognize the model if this keyword isn't included. It's removed before generation but still passed to the site.

async def get_models() -> dict:

    return {"data": [
        {"id": "llama-gpt-2-70b-chat"},
        {"id": "llama-gpt-2-13b-chat"},
        {"id": "llama-gpt-2-7b-chat"},
    ]}
