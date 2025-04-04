from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from db_utils import relatorio_csv_to_sql

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # Permite qualquer origem
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

def make_query(connection, query, params=None):
    if params is None:
        params = {}  # Garante que params nunca seja None
    return pd.read_sql_query(query, connection, params=params)

@app.route("/search", methods=["GET"])
def search_operators():
    # Reutilizando método de conexao com BD que carrega os arquivos csv em tabelas sql
    connection = relatorio_csv_to_sql()
    filters = {}

    reg = request.args.get("reg", "").strip().lower()
    cnpj = request.args.get("cnpj", "").strip().lower()
    corp_name =  request.args.get("corp_name", "").strip().lower()
    fantasy_name =  request.args.get("fantasy_name", "").strip().lower()
    modality = request.args.get("modality", "").strip().lower()
    city = request.args.get("city", "").strip().lower()
    state = request.args.get("state", "").strip().lower()
    sales_region = request.args.get("sales_region", "").strip().lower()

    query = "SELECT * FROM registros WHERE 1=1"  # 1=1 garante que podemos adicionar filtros sem erro

    if reg:
        query += " AND Registro_ANS = :reg"
        filters["reg"] = reg  # Adiciona o valor correspondente
    if cnpj:
        query += " AND CNPJ LIKE :cnpj"
        filters["cnpj"] = cnpj
    if corp_name:
        query += " AND LOWER(Razao_Social) LIKE :corp_name"
        filters["corp_name"] = f"%{corp_name}%" # Adiciona % para busca parcial
    if fantasy_name:
        query += " AND LOWER(Nome_Fantasia) LIKE :fantasy_name"
        filters["fantasy_name"] = f"%{fantasy_name}%"   
    if modality:
        query += " AND LOWER(Modalidade) LIKE :modality"
        filters["modality"] = modality
    if city:
        query += " AND LOWER(Cidade) LIKE :city"
        filters["city"] = f"%{city}%"
    if state:
        query += " AND LOWER(UF) = :state"
        filters["state"] = state
    if sales_region:
        query += " AND CAST(Regiao_de_Comercializacao AS TEXT) = :sales_region"
        filters["sales_region"] = str(sales_region)

    print("QUERY:", query)
    print("PARAMS:", filters)
    result = make_query(connection, query, filters)

    connection.close()

    # Retira valores NaN do dataframe
    result = result.where(pd.notnull(result), None)
    
    return jsonify(result.to_dict(orient="records"))
                    
app.run()