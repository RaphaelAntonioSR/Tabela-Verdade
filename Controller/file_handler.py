class FileHandler:
    """
    Classe responsável por manipular arquivos de fórmulas booleanas.
    """
    
    @staticmethod
    def read_fbfs_from_file(file_path):
        """
        Lê fórmulas booleanas bem formadas (FBFs) de um arquivo.
        
        Args:
            file_path (str): Caminho para o arquivo contendo as FBFs
            
        Returns:
            list: Lista de strings representando as FBFs lidas do arquivo
            
        Raises:
            ValueError: Se ocorrer um erro ao ler o arquivo
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Lê cada linha como uma FBF separada
                fbfs = [line.strip() for line in file.readlines() if line.strip()]
            return fbfs
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo: {str(e)}")