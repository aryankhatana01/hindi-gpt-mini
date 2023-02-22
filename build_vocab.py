import json
from tokenizer import HindiTokenizer

with open('input/combined.txt') as f:
    data = f.read()

tokenizer = HindiTokenizer()
data = tokenizer.trivial_tokenize(data)

distinct_tokens = list(set(data))

tok2ix = {
    token: idx for idx, token in enumerate(distinct_tokens)
}  # token to index

ix2tok = {
    idx: token  for idx, token in enumerate(distinct_tokens)
}  # index to token

with open('input/tok2ix.json', 'w') as f:  # save the token to index mapping
    json.dump(tok2ix, f)

with open('input/ix2tok.json', 'w') as f:  # save the index to token mapping
    json.dump(ix2tok, f)

# with open('input/vocab.json') as f:
#     data = json.load(f)

# print(data)