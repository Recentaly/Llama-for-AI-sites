# this file takes chat messages of OpenAI format and packs them to a single string

# messages argument should be in list type and should include dicts
async def msg_str(messages: list) -> str:

    # create an empty string we'll modify 
    output: str = ""

    start: str = "[INST]" # this is what's at the start of the user's prompt
    end: str = "[/INST]" # and this is at the end of the user's prompt

    # iterate through all the messages
    for message in messages:

        match message["role"]:

            case "user":

                output += f'{start} {message["content"]} {end}\n'

            case "assistant":

                output += f'{message["content"]}\n'

    # at the end, return the new string
    return output