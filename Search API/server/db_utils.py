import os
import sqlite3
import pandas as pd
import numpy as np

# Diretório base do projeto
# Obtém o diretório do projeto (subindo 2 níveis do diretório)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Caminho do arquivo CSV dentro da pasta BD
CSV_PATH = os.path.join(BASE_DIR, "BD", "Relatorio_cadop.csv")
print(CSV_PATH)

# Cria um banco de dados SQLite e carrega os registros do CSV na tabela 'registros'.
def relatorio_csv_to_sql():
    connection = sqlite3.connect(":memory:")  # Banco temporário em memória

    # Carregar o CSV
    df = pd.read_csv(CSV_PATH, delimiter=";")
    df = df.replace({np.nan: None})
    # Inserir os dados no banco
    df.to_sql("registros", connection, index=False, if_exists="replace")

    return connection