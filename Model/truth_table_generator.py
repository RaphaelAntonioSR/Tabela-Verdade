import pandas as pd
from itertools import product

class TruthTableGenerator:
    def __init__(self, formula_handler):
        self.formula_handler = formula_handler

    def evaluate(self, node, variables):
        if isinstance(node, tuple):
            op = node[0]
            args = [self.evaluate(arg, variables) for arg in node[1:]]
            return op(*args)
        elif isinstance(node, str):
            return variables[node]
        else:
            raise ValueError(f"Nó incorreto: {node}")

    def generate_truth_table(self, expression, variables):
        # Obter todas as subfórmulas
        subformulas = self.formula_handler.get_subformulas(expression)
        
        # Ordenar subfórmulas por complexidade (comprimento da string)
        sorted_subformulas = sorted(subformulas, key=lambda x: len(x[0]))
        
        # Preparar colunas para a tabela
        columns = variables.copy()
        subformula_nodes = {}
        
        # Adicionar colunas para cada subfórmula
        for subformula_str, subformula_node in sorted_subformulas:
            columns.append(subformula_str)
            subformula_nodes[subformula_str] = subformula_node
        
        # Gerar todas as combinações de valores verdade
        rows = []
        for values in product([0, 1], repeat=len(variables)):
            # Criar dicionário de valores para as variáveis
            local_vars = {var: bool(val) for var, val in zip(variables, values)}
            
            # Iniciar a linha com os valores das variáveis
            row = list(values)
            
            # Avaliar cada subfórmula
            for subformula_str, subformula_node in sorted_subformulas:
                result = self.evaluate(subformula_node, local_vars)
                row.append(int(result))
            
            rows.append(row)
        
        # Criar DataFrame
        return pd.DataFrame(rows, columns=columns)

    def classify_fbf(self, table, final_column):
        all_true = all(table[final_column] == 1)
        all_false = all(table[final_column] == 0)
        
        if all_true:
            return "Tautologia: A fórmula é sempre verdadeira para qualquer valoração das variáveis."
        elif all_false:
            return "Contradição: A fórmula é sempre falsa para qualquer valoração das variáveis."
        else:
            return "Contingência: A fórmula pode ser verdadeira ou falsa, dependendo da valoração das variáveis."