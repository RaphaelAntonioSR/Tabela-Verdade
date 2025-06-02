class LogicalOperations:
    """
    Classe que implementa operações lógicas básicas para manipulação de fórmulas booleanas.
    Fornece métodos estáticos para operações como AND, OR, NOT, XOR, equivalência e implicação.
    """
    
    @staticmethod
    def and_op(a, b):
        """
        Realiza a operação lógica AND (conjunção) entre dois valores booleanos.
        
        Args:
            a (bool): Primeiro operando booleano
            b (bool): Segundo operando booleano
            
        Returns:
            bool: Resultado da operação AND (a ∧ b)
        """
        return a and b

    @staticmethod
    def or_op(a, b):
        """
        Realiza a operação lógica OR (disjunção) entre dois valores booleanos.
        
        Args:
            a (bool): Primeiro operando booleano
            b (bool): Segundo operando booleano
            
        Returns:
            bool: Resultado da operação OR (a v b)
        """
        return a or b

    @staticmethod
    def not_op(a):
        """
        Realiza a operação lógica NOT (negação) de um valor booleano.
        
        Args:
            a (bool): Operando booleano
            
        Returns:
            bool: Resultado da operação NOT (~a)
        """
        return not a

    @staticmethod
    def xor_op(a, b):
        """
        Realiza a operação lógica XOR (ou exclusivo) entre dois valores booleanos.
        
        Args:
            a (bool): Primeiro operando booleano
            b (bool): Segundo operando booleano
            
        Returns:
            bool: Resultado da operação XOR (a ⊻ b)
        """
        return a ^ b

    @staticmethod
    def eq_op(a, b):
        """
        Realiza a operação lógica de equivalência entre dois valores booleanos.
        
        Args:
            a (bool): Primeiro operando booleano
            b (bool): Segundo operando booleano
            
        Returns:
            bool: Resultado da operação de equivalência (a ↔ b)
        """
        return a == b

    @staticmethod
    def imp_op(a, b):
        """
        Realiza a operação lógica de implicação entre dois valores booleanos.
        
        Args:
            a (bool): Primeiro operando booleano (antecedente)
            b (bool): Segundo operando booleano (consequente)
            
        Returns:
            bool: Resultado da operação de implicação (a → b)
        """
        return not a or b
    
    @classmethod
    def get_operations_info(cls):
        """
        Retorna informações sobre as operações lógicas disponíveis.
        
        Returns:
            list: Lista de tuplas contendo (símbolo, nome, descrição) para cada operação
        """
        return [
            ("∧", "AND", "Conjunção (E)"),
            ("v", "OR", "Disjunção (OU)"),
            ("~", "NOT", "Negação (NÃO)"),
            ("x", "XOR", "Ou Exclusivo"),
            ("↔", "EQUIV", "Equivalência (se e somente se)"),
            ("→", "IMPL", "Implicação (se... então...)"),
        ]