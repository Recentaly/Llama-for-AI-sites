# this function will return the system message from a list of messages
async def get_system_message(messages: list) -> str:

    return messages[0]["content"]