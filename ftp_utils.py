# ftp_utils.py

import os
from ftplib import FTP
from config import DIRETORIO_DESTINO

def criar_diretorio(diretorio):
    """Cria o diretório de destino se ele não existir"""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f"Diretório criado: {diretorio}")

def conectar_ftp():
    """Conecta ao FTP do IBGE"""
    print("Conectando ao FTP do IBGE...")
    ftp = FTP("ftp.ibge.gov.br")
    ftp.login()
    print("Conexão estabelecida com sucesso!")
    return ftp

def listar_arquivos_zip(ftp):
    """
    Lista arquivos ZIP no diretório atual do FTP.
    Usa MLSD se disponível, senão NLST.
    """
    try:
        arquivos = []
        for nome, attrs in ftp.mlsd():
            if nome.lower().endswith('.zip'):
                arquivos.append(nome)
        if arquivos:
            print(f"  (Usando MLSD - encontrados {len(arquivos)} arquivos)")
            return sorted(arquivos)
    except:
        print("  (MLSD não suportado, usando NLST)")
    
    try:
        arquivos = [f for f in ftp.nlst() if f.lower().endswith('.zip')]
        return sorted(arquivos)
    except Exception as e:
        print(f"  Erro ao listar arquivos: {e}")
        return []

def baixar_zip(ftp, nome_zip):
    """
    Baixa um arquivo ZIP do FTP para o diretório destino.
    Se já existir localmente, não baixa novamente.
    """
    caminho_zip = os.path.join(DIRETORIO_DESTINO, nome_zip)
    if os.path.exists(caminho_zip):
        print(f"✔ Arquivo já existe: {caminho_zip}")
        return caminho_zip
    
    print(f"↓ Baixando {nome_zip}...")
    with open(caminho_zip, "wb") as f:
        ftp.retrbinary(f"RETR {nome_zip}", f.write)
    print(f"  ✓ Download concluído: {caminho_zip}")
    return caminho_zip
