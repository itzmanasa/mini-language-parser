import ply.lex as lex

tokens = ('NUMBER', 'PLUS')
t_PLUS = r'\+'
t_ignore = ' \t\n'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal character:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input("12 + 3 + 45")

for token in lexer:
    print(token)
