# processing.py

import zipfile
import pandas as pd
from config import COL_NOMES, COL_LARGURAS, ESTADOS_ALVO

def processar_zip(caminho_zip):
    """
    Abre um arquivo ZIP, extrai o TXT e retorna um DataFrame filtrado pelos estados alvo.
    Também exibe relatório de valores nulos.
    """
    try:
        with zipfile.ZipFile(caminho_zip) as z:
            arquivos_txt = [f for f in z.namelist() if f.endswith(".txt")]
            if not arquivos_txt:
                print(f"⚠ Nenhum arquivo .txt encontrado em {caminho_zip}")
                return None
            
            nome_txt = arquivos_txt[0]
            with z.open(nome_txt) as f:
                df = pd.read_fwf(
                    f,
                    widths=COL_LARGURAS,
                    names=COL_NOMES,
                    dtype=str
                )
                
                # Filtrar pelos estados alvo
                df_filtrado = df[df["UF"].isin(ESTADOS_ALVO)].copy()
                print(f"✓ {len(df_filtrado):,} registros de PR/ES processados em {caminho_zip}")
                
                # Relatório de valores nulos
                null_counts = df_filtrado.isnull().sum()
                null_counts = null_counts[null_counts > 0]
                if not null_counts.empty:
                    print("🔎 Valores nulos detectados:")
                    print(null_counts)
                
                return df_filtrado
    except Exception as e:
        print(f"✗ Erro ao processar {caminho_zip}: {str(e)}")
        return None
