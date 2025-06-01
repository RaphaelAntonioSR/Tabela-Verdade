class LogicalOperations:
    @staticmethod
    def and_op(a, b):
        return a and b

    @staticmethod
    def or_op(a, b):
        return a or b

    @staticmethod
    def not_op(a):
        return not a

    @staticmethod
    def xor_op(a, b):
        return a ^ b

    @staticmethod
    def eq_op(a, b):
        return a == b

    @staticmethod
    def imp_op(a, b):
        return not a or b
    
    @classmethod
    def get_operations_info(cls):
        return [
            ("∧", "AND", "Conjunção (E)"),
            ("v", "OR", "Disjunção (OU)"),
            ("~", "NOT", "Negação (NÃO)"),
            ("x", "XOR", "Ou Exclusivo"),
            ("↔", "EQUIV", "Equivalência (se e somente se)"),
            ("→", "IMPL", "Implicação (se... então...)"),
        ]