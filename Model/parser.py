from Model.logical_operations import LogicalOperations

class Parser:
    """
    Classe responsável por analisar e converter expressões lógicas tokenizadas
    em uma estrutura de árvore que pode ser avaliada.
    """
    
    def __init__(self, tokens, variables):
        """
        Inicializa o parser com tokens e variáveis.
        
        Args:
            tokens (list): Lista de tokens da expressão
            variables (list): Lista de variáveis na expressão
        """
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
        """
        Analisa a expressão completa.
        
        Returns:
            tuple ou str: Árvore de análise representando a expressão
        """
        return self.parse_expression()

    def parse_expression(self):
        """
        Analisa uma expressão completa.
        
        Returns:
            tuple ou str: Árvore de análise representando a expressão
        """
        return self.parse_binary(0)

    def parse_binary(self, min_precedence):
        """
        Analisa uma expressão binária com precedência mínima.
        
        Args:
            min_precedence (int): Precedência mínima para operadores
            
        Returns:
            tuple ou str: Árvore de análise representando a expressão binária
        """
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
        """
        Analisa uma expressão unária (negação).
        
        Returns:
            tuple ou str: Árvore de análise representando a expressão unária
        """
        if self.current() == '~':
            self.advance()
            operand = self.parse_unary()
            return (LogicalOperations.not_op, operand)
        return self.parse_primary()

    def parse_primary(self):
        """
        Analisa uma expressão primária (variável ou expressão entre parênteses).
        
        Returns:
            tuple ou str: Árvore de análise representando a expressão primária
            
        Raises:
            ValueError: Se houver um erro de sintaxe na expressão
        """
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
        """
        Retorna o token atual.
        
        Returns:
            str ou None: O token atual ou None se não houver mais tokens
        """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        """
        Avança para o próximo token.
        """
        self.pos += 1
