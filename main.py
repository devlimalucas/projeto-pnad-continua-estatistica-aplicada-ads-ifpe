# main.py

import os
import zipfile
import sqlite3
from config import ANOS, DIRETORIO_DESTINO
from ftp_utils import conectar_ftp, criar_diretorio, listar_arquivos_zip
from processing import processar_zip
from database import salvar_sqlite_por_estado, exportar_resumo_por_estado, exportar_csv_por_estado

def limpar_bancos():
    """
    Limpa os bancos antes da execução: se já existem, apaga a tabela pnadc.
    """
    bancos = ["pnadc_es.db", "pnadc_pr.db"]

    for banco in bancos:
        if os.path.exists(banco):
            conn = sqlite3.connect(banco)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS pnadc")
            conn.commit()
            conn.close()
            print(f"⚠ Banco {banco} limpo antes da execução.")

def extrair_semestre_ano(nome_zip):
    """
    Extrai trimestre e ano a partir do nome do arquivo ZIP.
    Exemplo: PNADC_012023_20250815.zip -> (2023, 1)
    """
    try:
        partes = nome_zip.split("_")
        # Procura explicitamente um bloco de 6 dígitos (trimestre+ano)
        for parte in partes:
            if parte.isdigit() and len(parte) == 6:
                trimestre = int(parte[:2])
                ano = int(parte[2:])
                return ano, trimestre
        print(f"⚠ Não foi possível identificar ano/trimestre em {nome_zip}")
        return (9999, 99)  # fallback seguro
    except Exception as e:
        print(f"⚠ Erro ao extrair ano/trimestre de {nome_zip}: {e}")
        return (9999, 99)  # fallback seguro

def tentar_reconectar():
    """Tenta reconectar ao FTP até 3 vezes"""
    for tentativa in range(3):
        try:
            print(f"Tentando reconectar... tentativa {tentativa+1}")
            ftp = conectar_ftp()
            return ftp
        except Exception as e:
            print(f"Falha na tentativa {tentativa+1}: {e}")
    return None

def baixar_com_retentativas(ftp, nome_zip):
    """Tenta baixar um arquivo, com reconexão e validação de integridade"""
    caminho_zip = os.path.join(DIRETORIO_DESTINO, nome_zip)
    caminho_tmp = caminho_zip + ".tmp"

    try:
        if ftp:
            with open(caminho_tmp, "wb") as f:
                ftp.retrbinary(f"RETR " + nome_zip, f.write)

            if zipfile.is_zipfile(caminho_tmp):
                os.rename(caminho_tmp, caminho_zip)
                return caminho_zip
            else:
                print(f"⚠ Arquivo {nome_zip} corrompido. Removendo e tentando novamente...")
                os.remove(caminho_tmp)
    except Exception as e:
        print(f"⚠ Erro ao baixar {nome_zip}: {e}")
        if os.path.exists(caminho_tmp):
            os.remove(caminho_tmp)
        ftp = tentar_reconectar()
        if ftp:
            try:
                with open(caminho_tmp, "wb") as f:
                    ftp.retrbinary(f"RETR " + nome_zip, f.write)
                if zipfile.is_zipfile(caminho_tmp):
                    os.rename(caminho_tmp, caminho_zip)
                    return caminho_zip
                else:
                    print(f"⚠ Arquivo {nome_zip} ainda inválido após reconexão.")
                    os.remove(caminho_tmp)
            except Exception as e2:
                print(f"⚠ Falha mesmo após reconexão: {e2}")
                if os.path.exists(caminho_tmp):
                    os.remove(caminho_tmp)

    return None

def processar_ibge():
    ftp = None
    try:
        limpar_bancos()
        ftp = conectar_ftp()
        criar_diretorio(DIRETORIO_DESTINO)

        for ano in sorted(ANOS):
            print(f"\n📂 Processando ano {ano}")
            pasta_ftp = f"/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/{ano}/"

            try:
                ftp.cwd(pasta_ftp)
                arquivos_zip = listar_arquivos_zip(ftp)
            except Exception as e:
                print(f"⚠ Erro ao acessar {ano}: {e}")
                ftp = tentar_reconectar()
                arquivos_zip = [f for f in os.listdir(DIRETORIO_DESTINO) if f.endswith(".zip") and f"_{ano}" in f]

            arquivos_local = [f for f in os.listdir(DIRETORIO_DESTINO) if f.endswith(".zip") and f"_{ano}" in f]
            arquivos_a_processar = list(set(arquivos_local + arquivos_zip))

            if not arquivos_a_processar:
                print(f"⚠ Nenhum arquivo ZIP encontrado para {ano}")
                continue

            # Ordena cronologicamente por ano e trimestre
            arquivos_a_processar.sort(key=lambda nome: extrair_semestre_ano(nome))
            trimestres_encontrados = set()

            for nome_zip in arquivos_a_processar:
                ano_sem, trimestre = extrair_semestre_ano(nome_zip)
                print(f"\n➡ Processando {ano_sem} - trimestre {trimestre}")
                caminho_zip = os.path.join(DIRETORIO_DESTINO, nome_zip)

                if not os.path.exists(caminho_zip):
                    caminho_zip = baixar_com_retentativas(ftp, nome_zip)

                if caminho_zip and os.path.exists(caminho_zip):
                    df = processar_zip(caminho_zip)
                    if df is not None and not df.empty:
                        salvar_sqlite_por_estado(df)
                        trimestres_encontrados.add(trimestre)
                else:
                    print(f"⚠ Arquivo {nome_zip} não disponível. Pulando...")

            faltando = {1, 2, 3, 4} - trimestres_encontrados
            while faltando:
                print(f"⚠ No ano {ano}, faltam os trimestres: {sorted(faltando)}")
                for nome_zip in arquivos_zip:
                    ano_sem, trimestre = extrair_semestre_ano(nome_zip)
                    if trimestre in faltando:
                        caminho_zip = baixar_com_retentativas(ftp, nome_zip)
                        if caminho_zip and os.path.exists(caminho_zip):
                            df = processar_zip(caminho_zip)
                            if df is not None and not df.empty:
                                salvar_sqlite_por_estado(df)
                                trimestres_encontrados.add(trimestre)
                faltando = {1, 2, 3, 4} - trimestres_encontrados

            print(f"✅ Todos os 4 trimestres do ano {ano} foram processados com sucesso.")

    finally:
        try:
            if ftp:
                ftp.quit()
                print("\n🔌 Conexão FTP encerrada.")
        except Exception:
            print("\n⚠ Conexão FTP já estava encerrada.")

    exportar_resumo_por_estado()
    exportar_csv_por_estado()

if __name__ == "__main__":
    print("="*50)
    print("INICIANDO DOWNLOAD DA PNAD CONTÍNUA")
    print(f"Anos alvo: {ANOS}")
    print("="*50)
    processar_ibge()
