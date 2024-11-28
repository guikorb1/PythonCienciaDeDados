import pandas as pd
import matplotlib.pyplot as plt

class AcidentesLitoralAnalyzer:
    def __init__(self, file_path):
        # Inicializa o analisador de acidentes com o caminho do arquivo.
        self.file_path = file_path
        self.df = None
    def carregar_csv(self, encoding='latin1', delimiter=';'):
        # Carrega o arquivo CSV em um DataFrame.
        try:
            self.df = pd.read_csv(self.file_path, encoding=encoding, delimiter=delimiter)
            print("Arquivo CSV carregado com sucesso!")
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.file_path} não encontrado.")
            exit()
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            exit()
    def verificar_coluna(self, coluna):
        # Verifica se uma coluna existe no DataFrame.
        if coluna not in self.df.columns:
            print(f"Erro: A coluna '{coluna}' não foi encontrada no arquivo CSV.")
            print("Colunas disponíveis:", self.df.columns)
            exit()
    def limpar_e_transformar_dados(self):
        # Limpa e transforma os dados:
        # - Converte a coluna 'horario' para datetime.
        # - Cria a coluna 'hora' com a hora extraída.
        # - Remove linhas com valores inválidos em 'horario'.
        try:
            self.df['horario'] = pd.to_datetime(self.df['horario'], format='%H:%M:%S', errors='coerce')
            self.df = self.df.dropna(subset=['horario'])  # Remove linhas com horário inválido
            self.df['hora'] = self.df['horario'].dt.hour
            print("Dados limpos e transformados com sucesso!")
        except Exception as e:
            print(f"Erro ao transformar os dados: {e}")
            exit()
    def filtrar_por_horario(self, inicio, fim):
        # Filtra os dados com base em um intervalo de horas.
        return self.df[self.df['hora'].between(inicio, fim)]
    def contar_acidentes_por_hora(self, df_filtrado):
        # Conta os acidentes por hora em um DataFrame filtrado.
        return df_filtrado.groupby('hora').size()
    def criar_grafico(self, dados, titulo, xlabel, ylabel):
        # Cria e exibe um gráfico de barras para os dados fornecidos.
        plt.figure(figsize=(12, 6))
        bars = plt.bar(dados.index, dados.values, color='skyblue')
        # Destacar o horário com mais acidentes
        max_value = dados.max()
        for bar in bars:
            if bar.get_height() == max_value:
                bar.set_color('orange')
        # Personalizar o gráfico
        plt.title(titulo, fontsize=16)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.xticks(range(dados.index.min(), dados.index.max() + 1),
                   labels=[f'{h:02d}:00' for h in range(dados.index.min(), dados.index.max() + 1)], fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        # Mostrar valores no topo de cada barra
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     str(bar.get_height()), ha='center', va='bottom', fontsize=10)
        plt.tight_layout()
        plt.show()
# Uso da classe
if __name__ == "__main__":
    # Inicializa o analisador com o caminho do arquivo
    file_path = 'acidentes_litoral.csv'
    analyzer = AcidentesLitoralAnalyzer(file_path)
    # Carrega o arquivo CSV
    analyzer.carregar_csv()
    # Verifica a existência da coluna 'horario'
    analyzer.verificar_coluna('horario')
    # Limpa e transforma os dados
    analyzer.limpar_e_transformar_dados()
    # Filtra os dados entre 00:00 e 12:00
    df_manha = analyzer.filtrar_por_horario(0, 12)
    # Conta os acidentes por hora
    acidentes_por_hora_manha = analyzer.contar_acidentes_por_hora(df_manha)
    # Cria o gráfico
    analyzer.criar_grafico(acidentes_por_hora_manha,
                           titulo='Distribuição de Acidentes entre 00:00 e 12:00',
                           xlabel='Hora do Dia',
                           ylabel='Número de Acidentes')
