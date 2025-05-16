# TOKEN TYPES
NUMBER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    "NUMBER", "PLUS", "MINUS", "MUL", "DIV", "LPAREN", "RPAREN", "EOF"
    )

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
    

# PARSER CLASS - parsing tokens into an expression tree
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}, expected: {token_type}")
    
    # method to parse the expression
    def factor(self):
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
        elif token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
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
    
    def expr(self):
        result = self.term()
        # loop to handle addition and subtraction
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result


def evaluate_expression(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.expr()

# run code
if __name__ == "__main__":
    while True:
        try:
            line = input("calc> ")
            if line.strip() == "":
                continue
            result = evaluate_expression(line)
            print(result)
        except Exception as e:
            print(f"Error: {e}")