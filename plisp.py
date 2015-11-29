import re
import uuid


class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = []

    def eval(self):
        return self.val


class NumberNode(Node):
    def eval(self):
        return self.val


class ListNode(Node):
    def eval(self):
        r = None
        for node in self.next:
            r = node.eval()
        return r


def add(a , b):
    return a + b


def sub(a, b):
    return a - b


def div(a, b):
    return a / b


def mult(a, b):
    return a * b


class OperatorNode(Node):
    operator_dict = {'+': add, '-': sub, '/': div, '*': mult}

    def eval(self):
        operator = self.operator_dict[self.val]
        return operator(self.next[0].eval(),self.next[1].eval())


symbol_table = {}
node_class_dict = {'(': ListNode, '+': OperatorNode, '-': OperatorNode, '/': OperatorNode, '*': OperatorNode}


def tokenize(chars):
    """
    :param chars: String of lisp code.
    :return: List of tokens.
    """
    strings = re.findall("'(.*?)'", chars, re.DOTALL)
    for s in strings:
        st_id = str(uuid.uuid4())
        chars = chars.replace(s, st_id)
        symbol_table[st_id] = s
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def pretty_p(token_list):
    for s in token_list:
        s = s.replace("'", '')
        print s if s not in symbol_table else repr(symbol_table[s]),
    print


# pretty_p(tokenize("(begin ('testing' define r 'hello world') (* pi (* r r)))"))


def parse(tokens):
    head = Node(tokens[0])
    stack = [head]
    for token in tokens[1:]:
        if token == '(':
            node = Node(token)
            stack[-1].next.append(node)
            stack.append(node)
        elif token == ')':
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1].next.append(Node(token))
    return head


def parse_r(tokens, i=0):
    token = tokens[i]
    if token != '(':
        try:
            j = int(token)
            return NumberNode(j), i
        except ValueError:
            pass
        try:
            f = float(token)
            return NumberNode(f), i
        except ValueError:
            pass
        return Node(token), i
    i += 1
    val_token = tokens[i]
    node_class = node_class_dict[val_token] if val_token in node_class_dict else Node
    node = node_class(val_token)
    while True:
        i += 1
        n, i = parse_r(tokens, i)
        if n.val == ')':
            break
        node.next.append(n)
    return node, i



# "(begin begin ('testing' define r 'hello world') (* pi (* r r))) begin (r(x(y(z))))"
n, i = parse_r(tokenize("(/ (+ 4 4) (* 2 2))"))
print n.eval()



