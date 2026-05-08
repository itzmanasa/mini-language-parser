import ply.lex as lex
import ply.yacc as yacc

# lexer

# reserved words
reserved = {
    'for': 'FOR',
    'Println': 'PRINTLN',
}

# token names
tokens = [
    'ID',
    'COLONEQ',
    'NUMBER',
    'LT',
    'INCR',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'DOT',
    'LPAREN',
    'RPAREN',
] + list(reserved.values())

# token regex patterns
t_COLONEQ   = r':='
t_LT        = r'<'
t_INCR      = r'\+\+'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_DOT       = r'\.'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check for reserved words
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ignored characters (space, tab, carriage return)
t_ignore = ' \t\r'

# tracking newlines for line number reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()


# parser

def p_for_loop(p):
    '''for_loop : FOR ID COLONEQ NUMBER SEMICOLON ID LT NUMBER SEMICOLON ID INCR LBRACE statement RBRACE'''
    init_var = p[2]
    condition_var = p[6]
    increment_var = p[10]
    start_val = p[4]
    end_val = p[8]
    
    # validating that all three variables are the same
    if init_var == condition_var == increment_var:
        print(f"Valid Go for-loop with variable '{init_var}' running from {start_val} to {end_val}")
        p[0] = {
            'type': 'for_loop',
            'variable': init_var,
            'start': start_val,
            'end': end_val,
            'body': p[13]
        }
    else:
        print(f"Error: Loop variable mismatch - init: '{init_var}', condition: '{condition_var}', increment: '{increment_var}'")
        p[0] = None

def p_statement(p):
    '''statement : ID DOT PRINTLN LPAREN ID RPAREN'''
    package = p[1]
    function = p[3]
    argument = p[5]
    
    print(f"Print statement detected: {package}.{function}({argument})")
    p[0] = {
        'type': 'print',
        'package': package,
        'function': function,
        'argument': argument
    }

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) at line {p.lineno}")
    else:
        print("Syntax error at end of file")

parser = yacc.yacc()

# test

test_input = '''
for i := 0; i < 5; i++ {
    fmt.Println(i)
}
'''

print("=" * 60)
print("Lexing and Parsing Go For Loop")
print("=" * 60)
print("\nInput:")
print(test_input)
print("=" * 60)

# show tokens
print("\nTokens:")
lexer.input(test_input)
for tok in lexer:
    print(f"  {tok.type:12} -> '{tok.value}'")

# reset lexer and parse
lexer = lex.lex()
print("\n" + "=" * 60)
print("Parsing:")
print("=" * 60)
result = parser.parse(test_input, lexer=lexer)

print("\n" + "=" * 60)
print("Parsing Result:")
print("=" * 60)
if result:
    import json
    print(json.dumps(result, indent=2))
else:
    print("Parsing failed")

# additional tests

print("\n\n" + "=" * 60)
print("Additional Test Cases")
print("=" * 60)

# test case 2: variable mismatch (should fail)
test_input_2 = '''
for i := 0; j < 5; i++ {
    fmt.Println(i)
}
'''

print("\n\nTest 2: Variable Mismatch")
print(test_input_2)
lexer = lex.lex()
result2 = parser.parse(test_input_2, lexer=lexer)

# test case 3: different loop range
test_input_3 = '''
for x := 10; x < 20; x++ {
    fmt.Println(x)
}
'''

print("\n\nTest 3: Different Loop Range")
print(test_input_3)
lexer = lex.lex()
result3 = parser.parse(test_input_3, lexer=lexer)
if result3:
    import json
    print(json.dumps(result3, indent=2))