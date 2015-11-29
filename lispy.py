
def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    tokens = []
    stack = []
    list_c = -1
    for c in chars:
        print stack 
        if c == '(' and len(stack) ==1 and tokens:
            tokens.append([''])
            list_c = len(tokens) - 1
        elif c == '(':
            tokens.append([''])
            list_c += 1
            stack.append(c)
        elif c == ')' and stack:
            stack.pop()
            list_c -= 1
        else:
            tokens[list_c].append(c)
    return [''.join(l) for l in tokens]    
#"(begin (define r 10) (* pi (* r r)))"
#"(begin('cory(is)))('here')"          
            


Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)


# test


ls = "(begin (define r 10) (* pi (* r r)))"
print tokenize(ls)
#print parse(ls)
