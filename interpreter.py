# ARITHMETIC TYPES
NUMBER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = "NUMBER", "PLUS", "MINUS", "MUL", "DIV", "LPAREN", "RPAREN", "EOF"    

# BOOLEAN TYPES
TRUE, FALSE = "TRUE", "FALSE"
AND, OR, NOT = "AND", "OR", "NOT"
EQ, NEQ, LT, GT, LTE, GTE = "EQ", "NEQ", "LT", "GT", "LTE", "GTE"

# TEXT TYPES
STRING = "STRING"

# GLOBAL TYPES
global_env = {}
IDENTIFIER, ASSIGN, PRINT = "IDENTIFIER", "ASSIGN", "PRINT"

# CONTROL FLOW TYPES
IF, ELSE, WHILE, LBRACE, RBRACE, INPUT = "IF", "ELSE", "WHILE", "LBRACE", "RBRACE", "INPUT"

# ADDING LISTS
LBRACKET, RBRACKET, COMMA = "LBRACKET", "RBRACKET", "COMMA"


# TOKEN CLASS - represents a single token
class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
    
    # method to return a string representation of the token
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
# LEXER CLASS - converting input to tokens
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    # method to get the next token from the input
    def get_next_token(self):
        # while loop to iterate through user input
        while self.pos < len(self.text):
            current = self.text[self.pos]
            
            # if statements for different token types to be recognized
            if current.isspace():
                self.pos += 1
                continue
            if current.isdigit() or current == '.':
                return self.number()
            if current == '+':
                self.pos += 1
                return Token(PLUS, '+')
            if current == '-':
                self.pos += 1
                return Token(MINUS, '-')
            if current == '*':
                self.pos += 1
                return Token(MUL, '*')
            if current == '/':
                self.pos += 1
                return Token(DIV, '/')
            if current == '(':
                self.pos += 1
                return Token(LPAREN, '(')
            if current == ')':
                self.pos += 1
                return Token(RPAREN, ')')
            
            # if statement for string types
            if current == '"':
                return self.string()
            
            # if statements for boolean types
            if self.text[self.pos:].startswith("true"):
                self.pos += 4
                return Token(TRUE, True)
            if self.text[self.pos:].startswith("false"):
                self.pos += 5
                return Token(FALSE, False)
            if self.text[self.pos:].startswith("and"):
                self.pos += 3
                return Token(AND)
            if self.text[self.pos:].startswith("or"):
                self.pos += 2
                return Token(OR)
            if self.text[self.pos:].startswith("not"):
                self.pos += 3
                return Token(NOT)
            if self.text[self.pos:].startswith("=="):
                self.pos += 2
                return Token(EQ)
            if self.text[self.pos:].startswith("!="):
                self.pos += 2
                return Token(NEQ)
            if self.text[self.pos:].startswith(">="):
                self.pos += 2
                return Token(GTE)
            if self.text[self.pos:].startswith("<="):
                self.pos += 2
                return Token(LTE)

            if current == '>':
                self.pos += 1
                return Token(GT)
            if current == '<':
                self.pos += 1
                return Token(LT)

            # if statement for identifiers
            if current == '=':
                self.pos += 1
                return Token(ASSIGN, '=')
            
            if self.text[self.pos:].startswith("print"):
                self.pos += 5
                return Token(PRINT)
            
            if current == '{':
                self.pos += 1
                return Token(LBRACE)

            if current == '}':
                self.pos += 1
                return Token(RBRACE)
            
            # if statements for list
            if current == '[':
                self.pos += 1
                return Token(LBRACKET)
            if current == ']':
                self.pos += 1
                return Token(RBRACKET)
            if current == ',':
                self.pos += 1
                return Token(COMMA)

            # identifier, var names
            if current.isalpha():
                return self.identifier()
                     
            # error for if an invalid character is found
            raise Exception(f"Invalid character: {current}")
        
        #return EOF token when end of input is reached
        return Token(EOF)
    
    # method to get a number token from the input
    def number(self):
        result = ''
        # loop to get the number
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            result += self.text[self.pos]
            self.pos += 1
        
        return Token(NUMBER, float(result))
    
    # method to get a string token from the input
    def string(self):
        self.pos += 1 # skips opening quote
        result = ""
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            result += self.text[self.pos]
            self.pos += 1
            
        if self.pos >= len(self.text):
            raise Exception("Unterminated string literal") # meaning user entered string without closing quote marks
        
        self.pos += 1 # skips closing quote
        return Token(STRING, result)
    
    def identifier(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isalnum():
            result += self.text[self.pos]
            self.pos += 1

        # Keyword detection
        keywords = {
            "if": IF,
            "else": ELSE,
            "while": WHILE,
            "input": INPUT,
            "print": PRINT,
            "true": TRUE,
            "false": FALSE,
        }

        if result in keywords:
            if result == "true":
                return Token(TRUE, True)
            elif result == "false":
                return Token(FALSE, False)
            return Token(keywords[result])
        
        return Token(IDENTIFIER, result)


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def get_next_token(self):
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        return Token(EOF)


# PARSER CLASS - parsing tokens into an expression tree
class Parser:
    def __init__(self, lexer, env):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
        self.env = env # global variable store
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}, expected: {token_type}")

    def parse_block(self):
        self.eat(LBRACE)
        while self.current_token.type != RBRACE:
            self.statement()
        self.eat(RBRACE)

    def if_statement(self):
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        if condition:
            self.parse_block()
            if self.current_token.type == ELSE:
                # skip the else block
                self.eat(ELSE)
                self.skip_block()
        else:
            self.skip_block()  # skip the if block
            if self.current_token.type == ELSE:
                self.eat(ELSE)
                self.parse_block()

    def while_statement(self):
        self.eat(WHILE)
        self.eat(LPAREN)
        condition_tokens = []

        # Capture the condition expression tokens
        paren_count = 1
        while paren_count > 0:
            token = self.current_token
            if token.type == LPAREN:
                paren_count += 1
            elif token.type == RPAREN:
                paren_count -= 1
            if paren_count > 0:
                condition_tokens.append(token)
            self.eat(token.type)  # advance token

        self.eat(LBRACE)

        # Capture block source
        block_tokens = []
        brace_count = 1
        while brace_count > 0:
            token = self.current_token
            if token.type == LBRACE:
                brace_count += 1
            elif token.type == RBRACE:
                brace_count -= 1
            if brace_count > 0:
                block_tokens.append(token)
            self.eat(token.type)

        # Execute while loop
        while True:
            condition_parser = Parser(TokenStream(condition_tokens), self.env.copy())
            if not condition_parser.expr():
                break
            block_parser = Parser(TokenStream(block_tokens), self.env)
            while block_parser.current_token.type != EOF:
                block_parser.statement()

    def skip_block(self):
        self.eat(LBRACE)
        brace_count = 1
        while brace_count > 0:
            token = self.current_token
            if token.type == LBRACE:
                brace_count += 1
            elif token.type == RBRACE:
                brace_count -= 1
            self.current_token = self.lexer.get_next_token()

    def list_expr(self):
        elements = []
        self.eat(LBRACKET)
        if self.current_token.type != RBRACKET:
            elements.append(self.expr())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                elements.append(self.expr())
        self.eat(RBRACKET)
        return elements


    def statement(self):
        if self.current_token.type == IF:
            self.if_statement()
            return None
        elif self.current_token.type == WHILE:
            self.while_statement()
            return None
        elif self.current_token.type == PRINT:
            self.eat(PRINT)
            value = self.expr()
            print(value)
            return None
        elif self.current_token.type == IDENTIFIER:
            var_name = self.current_token.value
            self.eat(IDENTIFIER)

            if self.current_token.type == LBRACKET:
                # List mutation
                self.eat(LBRACKET)
                index = self.expr()
                self.eat(RBRACKET)
                self.eat(ASSIGN)
                value = self.expr()

                if var_name in self.env:
                    target = self.env[var_name]
                    if isinstance(target, list):
                        target[int(index)] = value
                    else:
                        raise Exception(f"Variable '{var_name}' is not a list")
                else:
                    raise Exception(f"Undefined variable: {var_name}")
                return None  # Don't return value on assignment

            elif self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                value = self.expr()
                self.env[var_name] = value
                return None  # Don't return value on assignment

            elif var_name in self.env:
                return self.env[var_name]
            else:
                raise Exception(f"Undefined variable: {var_name}")

        else:
            return self.expr()

        
    def factor(self):
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
        elif token.type == STRING:
            self.eat(STRING)
            return token.value
        elif token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == TRUE:
            self.eat(TRUE)
            return True
        elif token.type == FALSE:
            self.eat(FALSE)
            return False
        elif token.type == NOT:
            self.eat(NOT)
            return not self.factor()
        elif token.type == IDENTIFIER:
            var_name = token.value
            self.eat(IDENTIFIER)
            value = self.env.get(var_name)
            if self.current_token.type == LBRACKET:
                self.eat(LBRACKET)
                index = self.expr()
                self.eat(RBRACKET)
                try:
                    return value[int(index)]
                except:
                    raise Exception(f"Invalid index access on {var_name}")
            return value
        elif token.type == LBRACKET:
            return self.list_expr()
        elif token.type == RBRACKET:
            self.eat(RBRACKET)
            return []            
        elif token.type == INPUT:
            self.eat(INPUT)
            self.eat(LPAREN)
            prompt = self.expr() if self.current_token.type != RPAREN else ""
            self.eat(RPAREN)
            return input(str(prompt))

        else:
            raise Exception(f"Invalid factor: {token}")
    
    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("Division by zero")
                result /= divisor
        return result
    
    def comparison(self):
        result = self.term()
        while self.current_token.type in (EQ, NEQ, LT, GT, LTE, GTE):
            token = self.current_token
            if token.type == EQ:
                self.eat(EQ)
                result = result == self.term()
            elif token.type == NEQ:
                self.eat(NEQ)
                result = result != self.term()
            elif token.type == LT:
                self.eat(LT)
                result = result < self.term()
            elif token.type == GT:
                self.eat(GT)
                result = result > self.term()
            elif token.type == LTE:
                self.eat(LTE)
                result = result <= self.term()
            elif token.type == GTE:
                self.eat(GTE)
                result = result >= self.term()
        return result

    def expr(self):
        result = self.comparison()
        while self.current_token.type in (AND, OR, PLUS, MINUS):  # added MINUS here
            token = self.current_token
            if token.type == AND:
                self.eat(AND)
                result = result and self.comparison()
            elif token.type == OR:
                self.eat(OR)
                result = result or self.comparison()
            elif token.type == PLUS:
                self.eat(PLUS)
                right = self.comparison()
                if isinstance(result, str) or isinstance(right, str):
                    result = str(result) + str(right)
                else:
                    result += right
            elif token.type == MINUS:
                self.eat(MINUS)
                right = self.comparison()
                if not (isinstance(result, (int, float)) and isinstance(right, (int, float))):
                    raise Exception(f"Invalid operand types for '-': {type(result)} and {type(right)}")
                result -= right

        return result



def evaluate_expression(text):
    lexer = Lexer(text)
    parser = Parser(lexer, global_env)
    return parser.statement()

# run code
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # File mode
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                code = f.read()
                lines = code.splitlines()

                # Merge multi-line blocks
                full_line = ""
                for line in lines:
                    full_line += line + "\n"
                    if full_line.count("{") == full_line.count("}"):
                        if full_line.strip():
                            evaluate_expression(full_line)
                        full_line = ""
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # REPL mode
        while True:
            try:
                line = input("calc> ")
                while line.count("{") > line.count("}"):
                    line += "\n" + input("... ")
                if line.strip() == "":
                    continue
                result = evaluate_expression(line)
                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")
