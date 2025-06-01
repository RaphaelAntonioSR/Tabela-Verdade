from Model.logical_operations import LogicalOperations

class Parser:
    def __init__(self, tokens, variables):
        self.tokens = tokens
        self.pos = 0
        self.variables = variables
        self.ops = {
            '^': LogicalOperations.and_op,
            'v': LogicalOperations.or_op,
            '~': LogicalOperations.not_op,
            'x': LogicalOperations.xor_op,
            '<->': LogicalOperations.eq_op,
            '->': LogicalOperations.imp_op,
        }
        self.precedence = {
            '<->': 0,
            '->': 1,
            'v': 2,
            'x': 3,
            '^': 4,
            '~': 5
        }
        self.op_symbols = {
            LogicalOperations.and_op: '∧',
            LogicalOperations.or_op: 'v',
            LogicalOperations.not_op: '~',
            LogicalOperations.xor_op: 'x',
            LogicalOperations.eq_op: '↔',
            LogicalOperations.imp_op: '→'
        }

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        return self.parse_binary(0)

    def parse_binary(self, min_precedence):
        left = self.parse_unary()
        
        while (self.current() in self.ops and 
               self.current() != '~' and 
               self.precedence[self.current()] >= min_precedence):
            op = self.current()
            op_precedence = self.precedence[op]
            self.advance()
            right = self.parse_binary(op_precedence + 1)
            left = (self.ops[op], left, right)
        
        return left

    def parse_unary(self):
        if self.current() == '~':
            self.advance()
            operand = self.parse_unary()
            return (LogicalOperations.not_op, operand)
        return self.parse_primary()

    def parse_primary(self):
        if self.current() == '(':
            self.advance()
            expr = self.parse_expression()
            if self.current() != ')':
                raise ValueError("Esperado parêntese de fechamento.")
            self.advance()
            return expr
        elif self.current() in self.variables:
            var = self.current()
            self.advance()
            return var
        else:
            raise ValueError(f"Token incorreto: {self.current()}")

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1
