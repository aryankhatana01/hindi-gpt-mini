import torch
import torch.nn as nn
from torch.nn import functional as F
from tokenizer import HindiTokenizer
from config import CFG
from model import GPTLanguageModel

with open('input/combined.txt', 'r') as f:
    data = f.read()

tokenizer = HindiTokenizer()

tokenized_data = tokenizer.trivial_tokenize(data)
encoded_data = tokenizer.tok2ix(tokenized_data)
# print(encoded_data)

data = torch.tensor(encoded_data, dtype=torch.long)
n = int(0.8*len(data)) # first 90% will be train, rest val
train_data = data[:n]
val_data = data[n:]

# data loading
def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - CFG.block_size, (CFG.batch_size,))
    x = torch.stack([data[i:i+CFG.block_size] for i in ix])
    y = torch.stack([data[i+1:i+CFG.block_size+1] for i in ix])
    x, y = x.to(CFG.device), y.to(CFG.device)
    return x, y

@torch.inference_mode()
def estimate_loss(model):
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(CFG.eval_iters)
        for k in range(CFG.eval_iters):
            X, Y = get_batch(split)
            _, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

model = GPTLanguageModel(vocab_size=CFG.vocab_size)
m = model.to(CFG.device)
# print the number of parameters in the model
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

optimizer = torch.optim.AdamW(model.parameters(), lr=CFG.learning_rate)

for iter in range(CFG.max_iters):
    # every once in a while evaluate the loss on train and val sets
    if iter % CFG.eval_interval == 0 or iter == CFG.max_iters - 1:
        losses = estimate_loss(model=m)
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # sample a batch of data
    xb, yb = get_batch('train')

    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()
