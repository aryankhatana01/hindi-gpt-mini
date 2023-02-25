import json
from tokenizer import HindiTokenizer

with open('input/combined_data.txt') as f:
    data = f.read()

tokenizer = HindiTokenizer()
data = tokenizer.trivial_tokenize(data)

distinct_tokens = list(set(data))

tok2ix = {
    token: idx+1 for idx, token in enumerate(distinct_tokens)
}  # token to index

tok2ix['\n'] = 0  # add a token for newline

ix2tok = {
    idx+1: token  for idx, token in enumerate(distinct_tokens)
}  # index to token

ix2tok[0] = '\n'  # add a token for newline

with open('input/tok2ix.json', 'w') as f:  # save the token to index mapping
    json.dump(tok2ix, f)

with open('input/ix2tok.json', 'w') as f:  # save the index to token mapping
    json.dump(ix2tok, f)

# with open('input/vocab.json') as f:
#     data = json.load(f)

# print(data)