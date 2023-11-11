# the 'keys' are strings made by replicate.com to identify models

# this function transform a long string and returns the equivalent model in a more readable string
async def decrypt_model(key: str) -> str:

    match key:

        case "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3":

            return "llama-2-70b-chat"
        
        case "f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d":

            return "llama-2-13b-chat"
        
        case "13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0":

            return "llama-2-7b-chat"
        
# this function reverses the process above
async def encrypt_model(name: str):

    match name:

        case "llama-2-70b-chat":

            return "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"

        case "llama-2-13b-chat":

            return "f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

        case "llama-2-7b-chat":

            return "13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0"
