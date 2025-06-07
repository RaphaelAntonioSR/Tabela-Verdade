# Calculadora de Tabela Verdade - Documentação
## Visão Geral
A Calculadora de Tabela Verdade é uma aplicação Python que permite aos usuários criar, visualizar e analisar tabelas verdade para expressões lógicas. O programa suporta diversas operações lógicas, incluindo conjunção (AND), disjunção (OR), negação (NOT), implicação, equivalência e ou-exclusivo (XOR). A aplicação possui uma interface gráfica amigável e permite carregar fórmulas de arquivos de texto.

## Estrutura do Projeto
O projeto segue uma arquitetura MVC (Model-View-Controller):

- Model : Contém a lógica de processamento das expressões lógicas
- View : Implementa a interface gráfica do usuário
- Controller : Gerencia a interação entre o modelo e a visualização

## Como Rodar o código no UBUNTO 22.04
1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Abra o terminal
3. Certifique-se de estar na pasta do projeto
4. Execute o comando:

        pip install -r requirements.txt

5. Execute um dos dois comandos:

        python3 main.py
        python main.py


### Arquivos Principais
- main.py : Ponto de entrada da aplicação
- View/gui.py : Interface gráfica do usuário
- Model/expression_processor.py : Processamento de expressões lógicas
- Model/parser.py : Análise sintática das expressões
- Model/formula_handler.py : Manipulação de fórmulas lógicas
- Model/truth_table_generator.py : Geração de tabelas verdade
- Model/logical_operations.py : Implementação das operações lógicas
- Controller/file_handler.py : Manipulação de arquivos de fórmulas

## Funcionalidades
### Operações Lógicas Suportadas
| Símbolo | Operação     | Descrição         |
|---------|--------------|-------------------|
| ∧       | AND          | Conjunção (E)     |
| v       | OR           | Disjunção (OU)    |
| ~       | NOT          | Negação (NÃO)     |
| x       | XOR          | Ou exclusivo      |
| →       | IMPLICATION  | Implicação        |
| ↔       | EQUIVALENCE  | Equivalência      |

### Tipos de Fórmulas
O sistema pode classificar fórmulas em três categorias:

1. Tautologia : Fórmula sempre verdadeira para qualquer valoração das variáveis
2. Contradição : Fórmula sempre falsa para qualquer valoração das variáveis
3. Contingência : Fórmula que pode ser verdadeira ou falsa, dependendo da valoração das variáveis

### Entrada de Expressões
Você pode inserir expressões lógicas de duas maneiras:

1. Digitando diretamente : Insira a expressão no campo de texto
2. Carregando de um arquivo : Clique em "Carregar de Arquivo" e selecione um arquivo .txt contendo fórmulas

### Sintaxe das Expressões
- Variáveis: Letras maiúsculas (P, Q, R, etc.)
- Operadores:
  - AND: ^ ou ∧
  - OR: v
  - NOT: ~
  - XOR: x
  - Implicação: -> ou →
  - Equivalência: <-> ou ↔
- Parênteses: ( e ) para agrupar expressões

### Exemplos de Expressões
- Simples: P ^ Q , P v Q , ~P
- Complexas: (P -> Q) ^ (Q -> R) -> (P -> R) , ~(P v Q) <-> (~P ^ ~Q)

## Arquivos de Exemplo
O projeto inclui vários arquivos de exemplo na pasta FBF/ :

- Formulas Simples.txt : Expressões básicas
- Tautologias.txt : Fórmulas sempre verdadeiras
- Contradicoes.txt : Fórmulas sempre falsas
- Contingencias.txt : Fórmulas que podem ser verdadeiras ou falsas
- Formulas complexas.txt : Expressões mais elaboradas
- Formulas com Multiplas Variaveis.txt : Expressões com várias variáveis
- Formulas com Multiplos Operadores.txt : Expressões com múltiplos operadores

## Requisitos
- Python 3.x
- Pandas
- Tkinter (geralmente incluído na instalação padrão do Python)
- Itertools (também incluído na instalação padrão do Python)

## Conclusão
A Calculadora de Tabela Verdade é uma ferramenta educacional útil para estudantes e professores de lógica matemática, ciência da computação e disciplinas relacionadas. Ela permite a visualização e análise de tabelas verdade para expressões lógicas de forma intuitiva e eficiente.