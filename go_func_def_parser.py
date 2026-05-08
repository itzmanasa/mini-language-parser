# go_func_def_parser.py
import ply.lex as lex
import ply.yacc as yacc


# tokens
reserved = {
    'func': 'FUNC',
    'return': 'RETURN',
}

tokens = [
    'ID', 'TYPE',
    'LPAREN', 'RPAREN', 'COMMA',
    'LBRACE', 'RBRACE',
    'PLUS', 'SEMICOLON', 'NUMBER'
] + list(reserved.values())

# token rules (order matters for regex patterns)
def t_TYPE(t):
    r'int|float|string|bool|void'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'
t_SEMICOLON = r';'

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()

# parser
def p_func_def(p):
    '''func_def : FUNC ID LPAREN param_list RPAREN TYPE LBRACE stmt_list RBRACE'''
    func_name = p[2]
    return_type = p[6]
    params = p[4] if p[4] else []
    statements = p[8] if p[8] else []
    
    print(f"Function Definition Detected: '{func_name}' returns {return_type}")
    print(f"   Parameters: {params}")
    print(f"   Statements: {len(statements)} statement(s)")
    
    p[0] = {
        'type': 'function',
        'name': func_name,
        'params': params,
        'return_type': return_type,
        'body': statements
    }

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
    p[0] = {'name': p[1], 'type': p[2]}

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt_list stmt
                 | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : RETURN expr SEMICOLON'''
    print(f"Return statement found: {p[2]}")
    p[0] = {'type': 'return', 'value': p[2]}

def p_expr_binop(p):
    '''expr : ID PLUS ID'''
    p[0] = {'type': 'binop', 'op': '+', 'left': p[1], 'right': p[3]}

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = {'type': 'number', 'value': p[1]}

def p_expr_id(p):
    '''expr : ID'''
    p[0] = {'type': 'identifier', 'name': p[1]}

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error near token '{p.value}' (type: {p.type})")
    else:
        print("Syntax error at end of input")

parser = yacc.yacc()

# test input
data = """func add(a int, b int) int {
    return a + b;
}"""

print("Lexing and Parsing Go Function Definition\n")
print(f"Input:\n{data}")
print("=" * 50 + "\n")

# test lexing first
print("Tokens:")
lexer.input(data)
tokens_list = []
for tok in lexer:
    tokens_list.append(tok)
    print(f"  {tok.type:10} -> '{tok.value}'")

# reset lexer and parse
lexer = lex.lex()
print("\nParsing:")
result = parser.parse(data, lexer=lexer)

print("\n" + "=" * 50)
print("Parsing completed successfully!")
print("\nAbstract Syntax Tree:")
import json
print(json.dumps(result, indent=2))