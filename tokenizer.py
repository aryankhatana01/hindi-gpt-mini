"""
Tokenizer for the Hindi Language in the Devnagri script.
Reference: https://github.com/anoopkunchukuttan/indic_nlp_library
"""
import string, re

class HindiTokenizer:
    def __init__(self):
        ### tokenizer patterns 
        self.triv_tokenizer_indic_pat = re.compile(r'(['+string.punctuation+r'\u0964\u0965'+r'])')
        self.triv_tokenizer_urdu_pat = re.compile(r'(['+string.punctuation+r'\u0609\u060A\u060C\u061E\u066A\u066B\u066C\u066D\u06D4'+r'])')

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



if __name__ == '__main__': 
    hindi_string = "हिंदी टोकनाइजर का उपयोग हिंदी भाषा के टेक्स्ट को टोकन बनाने के लिए किया जाता है।"
    print("Base String: ", hindi_string)

    tokenizer = HindiTokenizer()

    tokens = tokenizer.trivial_tokenize(hindi_string)
    print("Tokens: ", tokens)

    detokenized = tokenizer.trivial_detokenize(tokens)
    print("Detokenized: ", detokenized)
    print("Is the Decoded string same as the Encoded string: ", hindi_string == detokenized)
