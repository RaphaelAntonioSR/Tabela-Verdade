from Model.logical_operations import LogicalOperations

class FormulaHandler:
    def __init__(self, parser):
        self.parser = parser
        self.op_symbols = parser.op_symbols

    def get_subformulas(self, node, subformulas=None):
        if subformulas is None:
            subformulas = set()
        
        # Se o nó é uma tupla, é uma operação
        if isinstance(node, tuple):
            op = node[0]
            args = node[1:]
            
            # Recursivamente obter subfórmulas dos operandos
            for arg in args:
                self.get_subformulas(arg, subformulas)
            
            # Construir a representação textual da subfórmula
            if op == LogicalOperations.not_op:
                # Operador unário (negação)
                arg_str = self.node_to_string(args[0])
                if isinstance(args[0], tuple):
                    subformula = f"~({arg_str})"
                else:
                    subformula = f"~{arg_str}"
                subformulas.add((subformula, node))
            else:
                # Operadores binários
                left_str = self.node_to_string(args[0])
                right_str = self.node_to_string(args[1])
                
                # Adicionar parênteses se os operandos são operações complexas
                if isinstance(args[0], tuple):
                    left_str = f"({left_str})"
                if isinstance(args[1], tuple):
                    right_str = f"({right_str})"
                    
                subformula = f"{left_str} {self.op_symbols[op]} {right_str}"
                subformulas.add((subformula, node))
        
        return subformulas

    def node_to_string(self, node):
        if isinstance(node, str):
            return node
        elif isinstance(node, tuple):
            op = node[0]
            args = node[1:]
            
            if op == LogicalOperations.not_op:
                # Operador unário (negação)
                arg_str = self.node_to_string(args[0])
                if isinstance(args[0], tuple):
                    return f"~({arg_str})"
                else:
                    return f"~{arg_str}"
            else:
                # Operadores binários
                left_str = self.node_to_string(args[0])
                right_str = self.node_to_string(args[1])
                
                # Adicionar parênteses se os operandos são operações complexas
                if isinstance(args[0], tuple):
                    left_str = f"({left_str})"
                if isinstance(args[1], tuple):
                    right_str = f"({right_str})"
                    
                return f"{left_str} {self.op_symbols[op]} {right_str}"
        else:
            raise ValueError(f"Tipo de nó desconhecido: {type(node)}")