# following function is responsible for translating models from janitorai (generic chatgpt models) to llama models
async def convert(model: str) -> str:

    match model:

        case "gpt-3.5-turbo":

            return "llama-gpt-2-70b-chat"
        
        case "gpt-3.5-turbo-0613":

            return "llama-gpt-2-13b-chat"
        
        case "gpt-3.5-turbo-16k":

            return "llama-gpt-2-7b-chat"