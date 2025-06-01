import re

class ExpressionProcessor:
    @staticmethod
    def extract_variables(expression):
        # Encontra todas as letras na expressão
        all_chars = re.findall(r'[a-zA-Z]+', expression)
        # Filtra operadores conhecidos
        operators = ['v', '⊻', '^', '~', '→', '↔']
        # Retorna variáveis únicas em ordem alfabética
        variables = sorted(list(set([char for char in all_chars if char not in operators])))
        return variables

    @staticmethod
    def tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char in "()":
                tokens.append(char)
                i += 1
            elif char.isalpha():
                # Captura variáveis (letras)
                var = char
                i += 1
                while i < len(expression) and expression[i].isalnum():
                    var += expression[i]
                    i += 1
                tokens.append(var)
            elif char == "^":
                tokens.append("^")
                i += 1
            elif char == "~":
                tokens.append("~")
                i += 1
            elif char == "v":
                tokens.append("v")
                i += 1
            elif char == "-" and i + 1 < len(expression) and expression[i + 1] == ">":
                tokens.append("->")
                i += 2
            elif char == "<" and i + 2 < len(expression) and expression[i + 1] == "-" and expression[i + 2] == ">":
                tokens.append("<->")
                i += 3
            elif char.isspace():
                i += 1
            else:
                raise ValueError(f"Caractere incorreto: {char}")
        return tokens