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
            if current == '!':
                self.pos += 1
                return Token(NOT)

            # if statement for identifiers
            if current == '=':
                self.pos += 1
                return Token(ASSIGN, '=')
            
            if self.text[self.pos:].startswith("print"):
                self.pos += 5
                return Token(PRINT)
            
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
        return Token(IDENTIFIER, result)


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

    def statement(self):
        if self.current_token.type == IDENTIFIER:
            # Let full expression parsing handle it
            return self.expr()

                
        elif self.current_token.type == PRINT:
            self.eat(PRINT)
            value = self.expr()
            print(value)
            return None
        else:
            return self.expr()
        
    # method to parse the expression
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
            if var_name in self.env:
                return self.env[var_name]
        else:
            raise Exception(f"Invalid factor: {token}")
    
    def term(self):
        result = self.factor()
        # loop to handle multiplication and division
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
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
        while self.current_token.type in (AND, OR, PLUS):
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
        return result


def evaluate_expression(text):
    lexer = Lexer(text)
    parser = Parser(lexer, global_env)
    return parser.statement()

# run code
if __name__ == "__main__":
    while True:
        try:
            line = input("calc> ")
            if line.strip() == "":
                continue
            result = evaluate_expression(line)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")