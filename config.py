import torch
import json

with open("input/ix2tok.json") as f: 
    vocab = json.load(f)

class CFG:
    batch_size = 16 # how many independent sequences will we process in parallel?
    block_size = 256 # what is the maximum context length for predictions?
    max_iters = 5000
    eval_interval = 5
    learning_rate = 3e-4
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    eval_iters = 200
    n_embd = 384
    n_head = 2
    n_layer = 2
    dropout = 0.2
    vocab_size = len(vocab)
