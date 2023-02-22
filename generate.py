import torch
from model import GPTLanguageModel
from config import CFG
from tokenizer import HindiTokenizer

load_model = False # set to True to load a pretrained model
output_filename='hindi.txt'

######## Intialize the model and tokenizer ########
model = GPTLanguageModel(vocab_size=CFG.vocab_size)
tokenizer = HindiTokenizer()
##################################################

if load_model:
    model.load_state_dict(torch.load('model.pt'))

def save_generated_text(generated_text, filename='hindi.txt'):
    with open(filename, 'w') as f:
        f.write(generated_text)

m = model.to(CFG.device)

model.eval()
context = torch.zeros((1, 1), dtype=torch.long, device=CFG.device)
generated_tokens = m.generate(context, max_new_tokens=500)[0].tolist()

dec_gen_tokens = tokenizer.ix2tok(generated_tokens)
generated_text = tokenizer.trivial_detokenize(dec_gen_tokens)
save_generated_text(generated_text, output_filename)
print(f"Generated text saved to {output_filename}!")
