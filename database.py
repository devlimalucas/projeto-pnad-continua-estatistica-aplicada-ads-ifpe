# database.py

import sqlite3
import pandas as pd

def salvar_sqlite_por_estado(df):
    """
    Salva os dados em dois bancos separados: ES e PR.
    """
    df_es = df[df["UF"] == "32"]
    df_pr = df[df["UF"] == "41"]

    if not df_es.empty:
        conn_es = sqlite3.connect("pnadc_es.db")
        df_es.to_sql("pnadc", conn_es, if_exists="append", index=False)
        conn_es.close()
        print(f"✓ {len(df_es)} registros inseridos em pnadc_es.db")

    if not df_pr.empty:
        conn_pr = sqlite3.connect("pnadc_pr.db")
        df_pr.to_sql("pnadc", conn_pr, if_exists="append", index=False)
        conn_pr.close()
        print(f"✓ {len(df_pr)} registros inseridos em pnadc_pr.db")

def exportar_resumo_por_estado():
    """
    Exporta resumo dos dados por trimestre para cada estado.
    """
    for nome_db, uf in [("pnadc_es.db", "ES"), ("pnadc_pr.db", "PR")]:
        try:
            conn = sqlite3.connect(nome_db)
            query = """
            SELECT Ano,
                   Trimestre,
                   COUNT(*) as registros
            FROM pnadc
            GROUP BY Ano, Trimestre
            ORDER BY Ano, Trimestre
            """
            resumo = pd.read_sql(query, conn)
            conn.close()
            print(f"\n📊 Resumo do banco {uf}:")
            print(resumo)
        except Exception as e:
            print(f"✗ Erro ao gerar resumo para {uf}: {str(e)}")

def exportar_csv_por_estado():
    """
    Exporta os dados de cada estado para CSV.
    """
    for nome_db, nome_csv, uf in [
        ("pnadc_es.db", "pnadc_es.csv", "ES"),
        ("pnadc_pr.db", "pnadc_pr.csv", "PR")
    ]:
        try:
            conn = sqlite3.connect(nome_db)
            df = pd.read_sql("SELECT * FROM pnadc ORDER BY Ano, Trimestre", conn)
            conn.close()
            df.to_csv(nome_csv, index=False, encoding="utf-8")
            print(f"📁 CSV gerado para {uf}: {nome_csv}")
        except Exception as e:
            print(f"✗ Erro ao exportar CSV para {uf}: {str(e)}")
