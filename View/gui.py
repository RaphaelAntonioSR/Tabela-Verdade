import tkinter as tk
from tkinter import ttk, filedialog
import os
from Model.expression_processor import ExpressionProcessor
from Model.parser import Parser
from Model.formula_handler import FormulaHandler
from Model.truth_table_generator import TruthTableGenerator
from Controller.file_handler import FileHandler
from Model.logical_operations import LogicalOperations

class TruthTableGUI:
    """
    Classe responsável pela interface gráfica do usuário para a calculadora de tabela verdade.
    Permite a entrada de expressões lógicas, carregamento de fórmulas de arquivos e
    visualização de tabelas verdade com classificação de fórmulas.
    """
    
    def __init__(self):
        """
        Inicializa a interface gráfica.
        """
        self.selected_fbf = None
        self.expr_processor = ExpressionProcessor()
        
    def show_input_window(self):
        """
        Exibe a janela principal de entrada de dados.
        Permite ao usuário digitar uma expressão lógica ou carregar de um arquivo.
        """
        root = tk.Tk()
        root.title("Entrada de dados")
        root.configure(bg="#f0f0f0")

        # Frame principal com padding e borda
        main_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        # Título com estilo
        title_label = tk.Label(main_frame, text="Calculadora de Tabela Verdade", 
                              font=("Arial", 18, "bold"), fg="#0066cc", bg="#f0f0f0")
        title_label.pack(pady=(0, 20))

        # Frame para entrada de expressão
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill="x", pady=10)
        
        tk.Label(input_frame, text="Digite a expressão lógica:", 
                 font=("Arial", 14), bg="#f0f0f0").pack(anchor="w")
        
        expr_entry = tk.Entry(input_frame, font=("Arial", 14), width=30)
        expr_entry.pack(fill="x", pady=5)
        
        # Frame para botões de entrada
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill="x", pady=5)
        
        # Label para mostrar o arquivo selecionado
        file_label = tk.Label(buttons_frame, text="", font=("Arial", 12, "italic"),
                             fg="#666666", bg="#f0f0f0")
        file_label.pack(side="left", padx=10)
        
        # Mensagem de erro
        error_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
        error_label.pack(pady=10)
        
        def process_input():
            try:
                raw_expression = expr_entry.get()
                # Extrair variáveis automaticamente da expressão
                variables = self.expr_processor.extract_variables(raw_expression)
                tokens = self.expr_processor.tokenize(raw_expression)
                parser = Parser(tokens, variables)
                parsed_expression = parser.parse()
                
                formula_handler = FormulaHandler(parser)
                truth_table_gen = TruthTableGenerator(formula_handler)
                
                # Gerar tabela verdade com subfórmulas
                table = truth_table_gen.generate_truth_table(parsed_expression, variables)
                
                # Classificar a FBF
                final_column = table.columns[-1]
                classification = truth_table_gen.classify_fbf(table, final_column)
                
                self.show_truth_table(parsed_expression, variables, table, classification, formula_handler)
            except Exception as e:
                error_label["text"] = f"Erro: {e}"

        def load_from_file():
            try:
                file_path = filedialog.askopenfilename(
                    title="Selecione um arquivo de texto",
                    filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
                )
                
                if file_path:  # Se um arquivo foi selecionado
                    # Atualizar o label com o nome do arquivo
                    file_name = os.path.basename(file_path)
                    file_label["text"] = f"Arquivo: {file_name}"
                    
                    # Ler as FBFs do arquivo
                    file_handler = FileHandler()
                    fbfs = file_handler.read_fbfs_from_file(file_path)
                    
                    if not fbfs:
                        error_label["text"] = "O arquivo está vazio ou não contém FBFs válidas."
                        return
                    
                    # Se houver apenas uma FBF, usá-la diretamente
                    if len(fbfs) == 1:
                        self.selected_fbf = fbfs[0]
                    else:
                        # Mostrar janela de seleção
                        self.selected_fbf = self.show_fbf_selection(fbfs, file_name, root)
                    
                    if self.selected_fbf:  # Se uma FBF foi selecionada
                        # Atualizar o campo de entrada
                        expr_entry.delete(0, tk.END)
                        expr_entry.insert(0, self.selected_fbf)
                        
                        # Limpar mensagem de erro
                        error_label["text"] = ""
                    else:
                        error_label["text"] = "Nenhuma FBF foi selecionada."
            except Exception as e:
                error_label["text"] = f"Erro: {e}"
        
        # Botão para carregar de arquivo
        load_button = tk.Button(buttons_frame, text="Carregar de Arquivo", command=load_from_file,
                              font=("Arial", 12), bg="#4CAF50", fg="white",
                              activebackground="#45a049", activeforeground="white",
                              padx=10, pady=3)
        load_button.pack(side="left")

        # Frame para operações com borda e fundo colorido
        ops_frame = tk.Frame(main_frame, bg="#e6f2ff", bd=1, relief="solid")
        ops_frame.pack(fill="x", pady=15)
        
        # Título para operações
        tk.Label(ops_frame, text="Operações Lógicas", 
                 font=("Arial", 14, "bold"), fg="#0066cc", bg="#e6f2ff").pack(pady=(10, 5))
        
        # Tabela de operações em grid
        ops_grid = tk.Frame(ops_frame, bg="#e6f2ff")
        ops_grid.pack(padx=20, pady=10)
        
        # Definir operações em formato de tabela
        operations = LogicalOperations.get_operations_info()
        
        # Cabeçalhos
        headers = ["Símbolo", "Operação", "Descrição"]
        
        for col, header in enumerate(headers):
            tk.Label(ops_grid, text=header, font=("Arial", 12, "bold"), 
                     bg="#e6f2ff", fg="#0066cc").grid(row=0, column=col, padx=10, pady=5, sticky="w")
        
        # Linhas de operações
        for row, (symbol, op, desc) in enumerate(operations, start=1):
            tk.Label(ops_grid, text=symbol, font=("Arial", 12), bg="#e6f2ff").grid(row=row, column=0, padx=10, pady=3, sticky="w")
            tk.Label(ops_grid, text=op, font=("Arial", 12), bg="#e6f2ff").grid(row=row, column=1, padx=10, pady=3, sticky="w")
            tk.Label(ops_grid, text=desc, font=("Arial", 12), bg="#e6f2ff").grid(row=row, column=2, padx=10, pady=3, sticky="w")

        # Exemplo com estilo
        example_frame = tk.Frame(main_frame, bg="#f0f0f0")
        example_frame.pack(fill="x", pady=10)
        
        tk.Label(example_frame, text="Exemplo:", font=("Arial", 12, "bold"), 
                 fg="#006600", bg="#f0f0f0").pack(side="left", padx=(0, 5))
        tk.Label(example_frame, text="(P ^ ~Q) v (P ^ R)", font=("Arial", 12, "italic"), 
                 fg="#006600", bg="#f0f0f0").pack(side="left")

        # Botão com estilo
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        build_button = tk.Button(button_frame, text="Construir Tabela", command=process_input, 
                               font=("Arial", 14, "bold"), bg="#0066cc", fg="white", 
                               activebackground="#004c99", activeforeground="white", 
                               padx=15, pady=5)
        build_button.pack()

        # Adicionar menu de operadores
        self.add_operator_menu(main_frame, expr_entry)

        root.mainloop()

    def add_operator_menu(self, parent_frame, entry_widget):
        """
        Adiciona um menu de botões de operadores lógicos à interface.
        
        Args:
            parent_frame (tk.Frame): Frame pai onde o menu será adicionado
            entry_widget (tk.Entry): Widget de entrada onde os operadores serão inseridos
        """
        # Frame para os botões de operadores
        op_buttons_frame = tk.Frame(parent_frame, bg="#f0f0f0")
        op_buttons_frame.pack(fill="x", pady=10)
        
        tk.Label(op_buttons_frame, text="Operadores:", 
                 font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        
        # Grid para os botões
        buttons_grid = tk.Frame(op_buttons_frame, bg="#f0f0f0")
        buttons_grid.pack(fill="x")
        
        # Definir operadores e seus símbolos
        operators = [
            ("^", "AND"),
            ("v", "OR"),
            ("~", "NOT"),
            ("x", "XOR"),
            ("<->", "EQUIV"),
            ("->", "IMPL"),
            ("(", "Abre parêntese"),
            (")", "Fecha parêntese")
        ]
        
        # Função para inserir operador na posição do cursor
        def insert_operator(op):
            cursor_pos = entry_widget.index(tk.INSERT)
            entry_widget.insert(cursor_pos, op)
            entry_widget.focus_set()
        
        # Função para criar tooltip
        def create_tooltip(widget, text):
            def enter(event):
                x, y, _, _ = widget.bbox("insert")
                x += widget.winfo_rootx() + 25
                y += widget.winfo_rooty() + 25
                
                # Criar uma janela de tooltip
                tooltip = tk.Toplevel(widget)
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{x}+{y}")
                
                label = tk.Label(tooltip, text=text, justify="left",
                                background="#ffffe0", relief="solid", borderwidth=1,
                                font=("Arial", 10))
                label.pack(ipadx=3, ipady=2)
                
                widget.tooltip = tooltip
            
            def leave(event):
                if hasattr(widget, "tooltip"):
                    widget.tooltip.destroy()
            
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
        
        # Criar botões para cada operador
        for i, (op, desc) in enumerate(operators):
            row, col = divmod(i, 4)  # 4 botões por linha
            button = tk.Button(buttons_grid, text=op, font=("Arial", 12), 
                             width=3, height=1, command=lambda o=op: insert_operator(o))
            button.grid(row=row, column=col, padx=5, pady=5)
            create_tooltip(button, desc)

    def show_fbf_selection(self, fbfs, file_name, parent_window):
        """
        Exibe uma janela para seleção de uma FBF de uma lista.
        
        Args:
            fbfs (list): Lista de FBFs disponíveis para seleção
            file_name (str): Nome do arquivo de onde as FBFs foram carregadas
            parent_window (tk.Tk): Janela pai
            
        Returns:
            str: A FBF selecionada ou None se nenhuma foi selecionada
        """
        # Variável para armazenar a FBF selecionada
        selected_fbf = [None]  # Usar lista para poder modificar dentro das funções aninhadas
        
        def on_select():
            selection = fbf_listbox.curselection()
            if selection:
                index = selection[0]
                selected_fbf[0] = fbfs[index]
                selection_window.destroy()
        
        def on_double_click(event):
            on_select()
        
        # Criar janela de seleção como modal
        selection_window = tk.Toplevel(parent_window)
        selection_window.title("Selecionar FBF")
        selection_window.configure(bg="#f0f0f0")
        selection_window.geometry("600x400")
        selection_window.transient(parent_window)
        selection_window.grab_set()
        selection_window.protocol("WM_DELETE_WINDOW", lambda: selection_window.destroy())
        
        # Frame principal
        main_frame = tk.Frame(selection_window, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text=f"Selecione uma FBF do arquivo: {file_name}", 
                              font=("Arial", 14, "bold"), fg="#0066cc", bg="#f0f0f0")
        title_label.pack(pady=(0, 15))
        
        # Frame para a lista
        list_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox para mostrar as FBFs
        fbf_listbox = tk.Listbox(list_frame, font=("Arial", 12), 
                               yscrollcommand=scrollbar.set, 
                               selectbackground="#0066cc", 
                               selectforeground="white",
                               height=15)
        fbf_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=fbf_listbox.yview)
        
        # Adicionar FBFs à lista
        for i, fbf in enumerate(fbfs, 1):
            fbf_listbox.insert(tk.END, f"{i}. {fbf}")
        
        # Selecionar o primeiro item por padrão
        if fbfs:
            fbf_listbox.selection_set(0)
        
        # Vincular evento de duplo clique
        fbf_listbox.bind('<Double-1>', on_double_click)
        
        # Botão de confirmação
        confirm_button = tk.Button(main_frame, text="Selecionar", command=on_select, 
                                 font=("Arial", 12, "bold"), bg="#0066cc", fg="white", 
                                 activebackground="#004c99", activeforeground="white", 
                                 padx=15, pady=5)
        confirm_button.pack(pady=15)
        
        # Esperar até que a janela seja fechada
        parent_window.wait_window(selection_window)
        
        return selected_fbf[0]

    def show_truth_table(self, expression, variables, table, classification, formula_handler):
        """
        Exibe a tabela verdade para uma expressão lógica.
        
        Args:
            expression (tuple): Expressão lógica analisada
            variables (list): Lista de variáveis na expressão
            table (pandas.DataFrame): Tabela verdade gerada
            classification (str): Classificação da fórmula
            formula_handler (FormulaHandler): Manipulador de fórmulas para conversão de nós para string
        """
        root = tk.Tk()
        root.title("Tabela Verdade")
        root.configure(bg="#f5f5f5")
        
        main_frame = tk.Frame(root, padx=20, pady=20, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True)

        # Título com a expressão completa
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(fill="x", pady=10)
        
        tk.Label(title_frame, text="Tabela Verdade para a Expressão:", 
                 font=("Arial", 16, "bold"), fg="#0066cc", bg="#f5f5f5").pack()
        
        # Expressão formatada
        expr_str = formula_handler.node_to_string(expression)
        expr_label = tk.Label(title_frame, text=expr_str, 
                             font=("Arial", 14), fg="#333333", bg="#f5f5f5")
        expr_label.pack(pady=5)

        # Frame para a tabela
        table_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, pady=15)
        
        # Estilo para a tabela
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="#333333", rowheight=25, fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#e6f2ff", foreground="#0066cc")
        style.map("Treeview", background=[("selected", "#0066cc")])

        # Criar tabela com scrollbar
        table_container = tk.Frame(table_frame)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical")
        hsb = ttk.Scrollbar(table_container, orient="horizontal")
        
        tree = ttk.Treeview(table_container, columns=list(table.columns), show="headings", 
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)
        
        # Configurar colunas
        for i, col in enumerate(table.columns):
            # Variáveis com largura menor
            if i < len(variables):
                tree.heading(col, text=col)
                tree.column(col, width=60, anchor="center")
            else:
                # Subfórmulas com largura maior
                tree.heading(col, text=col)
                tree.column(col, width=min(200, len(col)*10), anchor="center")

        # Inserir dados
        for _, row in table.iterrows():
            # Converter valores para V/F para melhor visualização
            display_row = ["V" if val == 1 else "F" for val in row]
            tree.insert("", tk.END, values=display_row)

        # Classificação da FBF
        class_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=15)
        class_frame.pack(fill="x")
        
        # Determinar cor baseada na classificação
        class_color = "#006600"  # Verde para tautologia
        if "Contradição" in classification:
            class_color = "#cc0000"  # Vermelho para contradição
        elif "Contingência" in classification:
            class_color = "#ff6600"  # Laranja para contingência
        
        class_label = tk.Label(class_frame, text="Classificação da FBF:", 
                              font=("Arial", 14, "bold"), fg="#333333", bg="#f5f5f5")
        class_label.pack()
        
        result_label = tk.Label(class_frame, text=classification, 
                               font=("Arial", 14), fg=class_color, bg="#f5f5f5")
        result_label.pack(pady=5)

        # Botão de fechar
        close_button = tk.Button(main_frame, text="Fechar", command=root.destroy, 
                               font=("Arial", 14, "bold"), bg="#0066cc", fg="white", 
                               activebackground="#004c99", activeforeground="white", 
                               padx=15, pady=5, width=15)
        close_button.pack(pady=15)

        root.mainloop()
        