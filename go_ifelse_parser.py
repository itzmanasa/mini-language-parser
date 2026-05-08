import ply.lex as lex
import ply.yacc as yacc

# lexer

reserved = {
    'if': 'IF',
    'else': 'ELSE',
}

tokens = [
    'ID',
    'NUMBER',
    'GT',
    'LT',
    'EQ',
    'LBRACE', 'RBRACE',
] + list(reserved.values())

t_GT       = r'>'
t_LT       = r'<'
t_EQ       = r'=='
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

# parser

def p_if_stmt(p):
    '''if_stmt : IF condition LBRACE statement RBRACE
               | IF condition LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    if len(p) == 6:
        # If without else
        print(f"If statement detected")
        print(f"   Condition: {p[2]}")
        print(f"   Then block: {p[4]}")
        p[0] = {
            'type': 'if',
            'condition': p[2],
            'then_block': p[4],
            'else_block': None
        }
    else:
        # If-else
        print(f"If-Else statement detected")
        print(f"   Condition: {p[2]}")
        print(f"   Then block: {p[4]}")
        print(f"   Else block: {p[8]}")
        p[0] = {
            'type': 'if_else',
            'condition': p[2],
            'then_block': p[4],
            'else_block': p[8]
        }

def p_condition(p):
    '''condition : ID GT NUMBER
                 | ID LT NUMBER
                 | ID EQ NUMBER'''
    p[0] = {
        'left': p[1],
        'operator': p[2],
        'right': p[3]
    }

def p_statement(p):
    '''statement : ID
                 | empty'''
    if p[1] is not None:
        p[0] = {'type': 'identifier', 'name': p[1]}
    else:
        p[0] = None

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) at line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

# test cases

test_input_1 = '''
if x > 10 {
    y
} else {
    z
}
'''

test_input_2 = '''
if a < 5 {
    b
}
'''

test_input_3 = '''
if count == 0 {
    empty
} else {
    full
}
'''

print("=" * 60)
print("Testing Go If-Else Statement Parser")
print("=" * 60)

# test 1: if-else
print("\n Test 1: If-Else Statement")
print(test_input_1)
print("-" * 60)
result1 = parser.parse(test_input_1, lexer=lex.lex())
if result1:
    import json
    print("\nAST:")
    print(json.dumps(result1, indent=2))

# test 2: if only (no else)
print("\n\nTest 2: If Statement (no else)")
print(test_input_2)
print("-" * 60)
result2 = parser.parse(test_input_2, lexer=lex.lex())
if result2:
    import json
    print("\nAST:")
    print(json.dumps(result2, indent=2))

# Test 3: If-Else with equality
print("\n\nTest 3: If-Else with Equality")
print(test_input_3)
print("-" * 60)
result3 = parser.parse(test_input_3, lexer=lex.lex())
if result3:
    import json
    print("\nAST:")
    print(json.dumps(result3, indent=2))