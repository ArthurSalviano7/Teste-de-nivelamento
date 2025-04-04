import sqlite3
import pandas as pd
import os


# Método para criar a conexão e tabelas no BD a partir do csv
def csv_to_sqlite():
    connection = sqlite3.connect(":memory:")  # Cria um banco temporário na memória
    
    df1 = pd.read_csv("1T2024.csv", delimiter=";")
    df2 = pd.read_csv("2T2024.csv", delimiter=";")
    df3 = pd.read_csv("3T2024.csv", delimiter=";")
    df4 = pd.read_csv("4T2024.csv", delimiter=";")

    # Cria uma tabela para o 4º Trimestre
    df4.to_sql("despesas_4T", connection, index=False, if_exists="replace")

    # Realiza a concatenação dos 4 trimestres em uma só tabela
    df_concat = pd.concat([df1, df2, df3, df4], ignore_index=True)
    df_concat.to_sql("despesas_2024", connection, index=False, if_exists="replace")

    df = pd.read_csv("Relatorio_cadop.csv", delimiter=";")
    df.to_sql("registros", connection, index=False, if_exists="replace")
    
    return connection 

def make_query(connection, query):
    return pd.read_sql_query(query, connection)

def main():
    connection = csv_to_sqlite()
    
    print("\n10 operadoras com maiores despesas em 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'")
    print("\nÚltimo trimestre (4T2024):\n")
    result = make_query(connection, 
    ("SELECT r.Razao_Social, SUM(d.VL_SALDO_INICIAL - d.VL_SALDO_FINAL) AS VL_despesa_R$ "
    "FROM registros AS r LEFT JOIN despesas_4T AS d ON (r.Registro_ANS = d.REG_ANS) "
    "WHERE (d.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR ') "
    "AND (d.VL_SALDO_INICIAL > d.VL_SALDO_FINAL)"
    "GROUP BY r.Razao_Social "
    "ORDER BY VL_despesa_R$ DESC "
    "LIMIT 10"))
    print(result)

    print("\nÚltimo ano (2024):\n")
    result = make_query(connection, 
    ("SELECT r.Razao_Social, SUM(d.VL_SALDO_INICIAL - d.VL_SALDO_FINAL) AS VL_despesa_R$ "
    "FROM registros AS r LEFT JOIN despesas_2024 AS d ON (r.Registro_ANS = d.REG_ANS) "
    "WHERE (d.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR ') "
    "AND (d.VL_SALDO_INICIAL > d.VL_SALDO_FINAL)"
    "GROUP BY r.Razao_Social "
    "ORDER BY VL_despesa_R$ DESC "
    "LIMIT 10"))
    print(result)

if __name__ == "__main__":
    main()