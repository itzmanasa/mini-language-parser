# Mini Language Interpreter

A mini compiler front-end and interpreter prototype built using Python Lex-Yacc (PLY).

This project demonstrates lexical analysis, syntax parsing, AST generation, and basic interpretation for custom language constructs and Go-like syntax structures.

## Features

- Lexical analysis using PLY lexer
- Syntax parsing using grammar rules
- AST-style parse tree generation
- Function declaration and definition parsing
- Array declaration parsing
- For-loop parsing and validation
- If-Else statement parsing
- Switch-case interpretation
- Environment-based variable evaluation
- Basic semantic validation and error handling

## Technologies Used

- Python
- PLY (Python Lex-Yacc)

## Project Structure

```bash
go_array_parser.py       # Parses Go-style array declarations
go_for_parser.py         # Parses Go-style for loops
go_func_decl_parser.py   # Parses function declarations
go_func_def_parser.py    # Parses function definitions and AST generation
go_ifelse_parser.py      # Parses if-else statements
test.py                  # Mini language parser and interpreter
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Example

```bash
python test.py
```

## Concepts Demonstrated

- Compiler Design Fundamentals
- Lexical Analysis
- Syntax Analysis
- Abstract Syntax Trees (AST)
- Parsing Techniques
- Semantic Validation
- Simple Interpreter Execution