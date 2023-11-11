# import OpenAI token encoding module
from tiktoken import get_encoding

# function which returns an encoder
async def create_encoder(base: str = "cl100k_base"):

    return get_encoding(base)