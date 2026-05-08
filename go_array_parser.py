import ply.lex as lex
import ply.yacc as yacc

# reserved words
reserved = {
    'var': 'VAR',
}

tokens = [
    'ID',
    'ASSIGN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA',
    'NUMBER',
    'TYPE',
] + list(reserved.values())

t_ASSIGN    = r'='
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_COMMA     = r','

def t_TYPE(t):
    r'int|float|string|bool'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\r\n'

def t_error(t):
    print("Illegal character:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# parser

def p_array_decl(p):
    '''array_decl : VAR ID ASSIGN LBRACKET NUMBER RBRACKET TYPE LBRACE elements RBRACE'''
    print(f"Array '{p[2]}' declared with size {p[5]}, type {p[7]}, and elements {p[9]}")

def p_elements(p):
    '''elements : NUMBER
                | NUMBER COMMA elements'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]   # Append instead of insert

def p_error(p):
    if p:
        print("Syntax error at", p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# test case

test_input = 'var arr = [5]int{1,2,3,4,5,}'

print("Testing Go Array Declaration")
print(test_input)
parser.parse(test_input)