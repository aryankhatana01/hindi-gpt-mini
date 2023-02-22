"""
Tokenizer for the Hindi Language in the Devnagri script.
Reference: https://github.com/anoopkunchukuttan/indic_nlp_library
[I had to fix some bugs in the original code and remove redundant parts]
"""
import string, re
import json

class HindiTokenizer:
    def __init__(self):
        ### tokenizer patterns 
        self.triv_tokenizer_indic_pat = re.compile(r'(['+string.punctuation+r'\u0964\u0965'+r'])')

        ## detokenizer patterns 
        left_attach = r'!%)\]},.:;>?\u0964\u0965'
        right_attach = r'#$(\[{<@'
        lr_attach = r'-/\\'

        self.pat_la = re.compile(r'[ ](['+left_attach+r'])')
        self.pat_ra = re.compile(r'(['+right_attach+r'])[ ]')
        self.pat_lra = re.compile(r'[ ](['+lr_attach+r'])[ ]')
        self.pat_num_seq = re.compile(r'([0-9]+ [,.:/] )+[0-9]+')

    def trivial_tokenize(self, text: str): 
        tok_str = self.triv_tokenizer_indic_pat.sub(r' \1 ',text.replace('\t',' '))

        s = re.sub(r'[ ]+',' ',tok_str).strip(' ')
        
        new_s=''
        prev=0
        for m in self.pat_num_seq.finditer(s):
            start=m.start()
            end=m.end()
            if start>prev:
                new_s=new_s+s[prev:start]
                new_s=new_s+s[start:end].replace(' ','')
                prev=end
    
        new_s=new_s+s[prev:]
        s=new_s
        
        return s.split(' ')


    def trivial_detokenize(self, tokens: list): 
        s=" ".join(tokens)
        new_s=''
        prev=0
        for m in self.pat_num_seq.finditer(s):
            start=m.start()
            end=m.end()
            if start>prev:
                new_s=new_s+s[prev:start]
                new_s=new_s+s[start:end].replace(' ','')
                prev=end
    
        new_s=new_s+s[prev:]
        s=new_s

        s = self.pat_lra.sub('\\1',s)
        s = self.pat_la.sub('\\1',s)
        s = self.pat_ra.sub('\\1',s)

        alt_attach='\'"`'
        for punc in alt_attach: 
            cnt=0
            out_str=[]
            for c in s:
                if c == punc:
                    if cnt%2==0:
                        out_str.append('@RA')
                    else:
                        out_str.append('@LA')
                    cnt+=1    
                else:
                    out_str.append(c)

            s=''.join(out_str).replace('@RA ',punc).replace(' @LA',punc
                    ).replace('@RA',punc).replace('@LA',punc)

        return s

    def tok2ix(self, tokens: list): 
        with open("input/tok2ix.json") as f: 
            tok2ix_dict = json.load(f)
        return [tok2ix_dict[tok] for tok in tokens]

    def ix2tok(self, tokens: list): 
        with open("input/ix2tok.json") as f: 
            ix2tok_dict = json.load(f)
        return [ix2tok_dict[str(tok)] for tok in tokens]



if __name__ == "__main__": 
    hindi_string = "बस्ती-बस्ती दहशत किसने बो दी है"  # Getting a string from the dataset
    print("Base String: ", hindi_string)

    tokenizer = HindiTokenizer()  # Creating an instance of the tokenizer

    tokens = tokenizer.trivial_tokenize(hindi_string)  # Tokenizing the string
    print("Tokens: ", tokens)

    detokenized = tokenizer.trivial_detokenize(tokens)  # Detokenizing the tokens
    print("Detokenized: ", detokenized)
    print("Is the Decoded string same as the Encoded string: ", hindi_string == detokenized)  # Checking if the decoded string is same as the encoded string

    with open("hindi.txt", "w") as f:  # Writing the detokenized string to a file
        f.write(detokenized)

    enc_tokens = tokenizer.tok2ix(tokens)  # Encoding the tokens to indices
    print("Encoded Tokens: ", enc_tokens)

    dec_tokens = tokenizer.ix2tok(enc_tokens)  # Decoding the indices to back to tokens
    print("Decoded Tokens: ", dec_tokens)

    print("Are the tokens same after encoding and decoding: ", tokens == dec_tokens)  # Checking if the tokens are same after encoding and decoding
