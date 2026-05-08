# go_func_decl_parser.py
import ply.lex as lex
import ply.yacc as yacc

# tokens
reserved = {
    'func': 'FUNC',
}

tokens = [
    'ID', 'LPAREN', 'RPAREN',
    'COMMA', 'TYPE'
] + list(reserved.values())


# token rules (order matters for regex patterns)
def t_TYPE(t):
    r'int|float|string|bool|void'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# parser
def p_func_decl(p):
    '''func_decl : FUNC ID LPAREN param_list RPAREN TYPE'''
    print(f"Function Declaration Detected: '{p[2]}' returns {p[6]}")
    print(f"   Parameters: {p[4] if p[4] else 'none'}")

def p_param_list(p):
    '''param_list : param
                  | param COMMA param_list
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = [p[1]] + p[3]

def p_param(p):
    '''param : ID TYPE'''
    p[0] = (p[1], p[2])
    print(f"   Parameter: {p[1]} of type {p[2]}")

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error near token '{p.value}' (type: {p.type})")
    else:
        print("Syntax error at end of input")

parser = yacc.yacc()

# test case
data = """func add(a int, b int) int"""

print("=== Lexing and Parsing Go Function Declaration ===\n")
print(f"Input: {data}")
print("=" * 50 + "\n")

# test lexing first
print("Tokens:")
lexer.input(data)
for tok in lexer:
    print(f"  {tok.type:10} -> '{tok.value}'")

# reset lexer and parse
lexer = lex.lex()
print("\nParsing:")
result = parser.parse(data, lexer=lexer)
print("\nParsing completed successfully!")