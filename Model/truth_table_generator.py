import pandas as pd
from itertools import product

class TruthTableGenerator:
    """
    Classe responsável por gerar tabelas verdade para expressões lógicas.
    """
    
    def __init__(self, formula_handler):
        """
        Inicializa o gerador de tabela verdade.
        
        Args:
            formula_handler (FormulaHandler): Manipulador de fórmulas para processar subfórmulas
        """
        self.formula_handler = formula_handler

    def evaluate(self, node, variables):
        """
        Avalia uma expressão lógica para um conjunto específico de valores de variáveis.
        
        Args:
            node (tuple ou str): Nó da árvore de análise representando a expressão
            variables (dict): Dicionário mapeando nomes de variáveis para seus valores booleanos
            
        Returns:
            bool: Resultado da avaliação da expressão
            
        Raises:
            ValueError: Se o nó for de um tipo desconhecido
        """
        if isinstance(node, tuple):
            op = node[0]
            args = [self.evaluate(arg, variables) for arg in node[1:]]
            return op(*args)
        elif isinstance(node, str):
            return variables[node]
        else:
            raise ValueError(f"Nó incorreto: {node}")

    def generate_truth_table(self, expression, variables):
        """
        Gera uma tabela verdade para uma expressão lógica.
        
        Args:
            expression (tuple ou str): Expressão lógica analisada
            variables (list): Lista de variáveis na expressão
            
        Returns:
            pandas.DataFrame: Tabela verdade com todas as combinações de valores e resultados
        """
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
        """
        Classifica uma Fórmula Bem Formada (FBF) com base em sua tabela verdade.
        
        Args:
            table (pandas.DataFrame): Tabela verdade da fórmula
            final_column (str): Nome da coluna que contém os resultados finais da fórmula
            
        Returns:
            str: Classificação da fórmula (Tautologia, Contradição ou Contingência)
        """
        all_true = all(table[final_column] == 1)
        all_false = all(table[final_column] == 0)
        
        if all_true:
            return "Tautologia: A fórmula é sempre verdadeira para qualquer valoração das variáveis."
        elif all_false:
            return "Contradição: A fórmula é sempre falsa para qualquer valoração das variáveis."
        else:
            return "Contingência: A fórmula pode ser verdadeira ou falsa, dependendo da valoração das variáveis."