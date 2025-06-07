import re

class ExpressionProcessor:
    """
    Classe responsável pelo processamento de expressões lógicas.
    Fornece métodos para extrair variáveis e tokenizar expressões.
    """
    
    @staticmethod
    def extract_variables(expression):
        """
        Extrai as variáveis de uma expressão lógica.
        
        Args:
            expression (str): A expressão lógica a ser analisada
            
        Returns:
            list: Lista ordenada de variáveis únicas encontradas na expressão
        """
        # Encontra todas as letras na expressão
        all_chars = re.findall(r'[a-zA-Z]+', expression)
        # Filtra operadores conhecidos
        operators = ['v', '⊻', '^', '~', '→', '↔']
        # Retorna variáveis únicas em ordem alfabética
        variables = sorted(list(set([char for char in all_chars if char not in operators])))
        return variables

    @staticmethod
    def tokenize(expression):
        """
        Converte uma expressão lógica em uma lista de tokens.
        
        Args:
            expression (str): A expressão lógica a ser tokenizada
            
        Returns:
            list: Lista de tokens da expressão
            
        Raises:
            ValueError: Se a expressão contiver caracteres inválidos ou múltiplas variáveis sem operadores
        """
        tokens = []
        i = 0
        last_token_type = None  # Para rastrear o tipo do último token
        
        while i < len(expression):
            char = expression[i]
            if char in "()":
                tokens.append(char)
                last_token_type = "parenthesis"
                i += 1
            elif char.isalpha():
                # Captura variáveis (letras)
                var = char
                i += 1
                while i < len(expression) and expression[i].isalnum():
                    var += expression[i]
                    i += 1
                
                # Verifica se o último token também era uma variável
                if last_token_type == "variable":
                    raise ValueError("Falta de operador na expressão")
                
                tokens.append(var)
                last_token_type = "variable"
            elif char == "^":
                tokens.append("^")
                last_token_type = "operator"
                i += 1
            elif char == "~":
                tokens.append("~")
                last_token_type = "operator"
                i += 1
            elif char == "v":
                tokens.append("v")
                last_token_type = "operator"
                i += 1
            elif char == "-" and i + 1 < len(expression) and expression[i + 1] == ">":
                tokens.append("->")
                last_token_type = "operator"
                i += 2
            elif char == "<" and i + 2 < len(expression) and expression[i + 1] == "-" and expression[i + 2] == ">":
                tokens.append("<->")
                last_token_type = "operator"
                i += 3
            elif char.isspace():
                i += 1
            else:
                raise ValueError(f"Caractere incorreto: {char}")
        return tokens