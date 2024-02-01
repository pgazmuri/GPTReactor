

import tiktoken
from cg_utilities import get_npm_errors

enc = tiktoken.encoding_for_model("gpt-4")
encoded = enc.encode("Hello world, let's test tiktoken.")
total_tokens = len(encoded)

print(total_tokens)
