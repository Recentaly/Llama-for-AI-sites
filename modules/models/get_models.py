# this file returns a list of supported models with type dict
# example output: {"data": [{"id": "gpt.3-5-turbo"}, {"id": "gpt-4"}]}

async def get_models() -> dict:

    return {"data": [
        {"id": "llama-gpt-2-70b-chat"},
        {"id": "llama-gpt-2-13b-chat"},
        {"id": "llama-gpt-2-7b-chat"},
    ]}