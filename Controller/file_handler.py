class FileHandler:
    @staticmethod
    def read_fbfs_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Lê cada linha como uma FBF separada
                fbfs = [line.strip() for line in file.readlines() if line.strip()]
            return fbfs
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo: {str(e)}")