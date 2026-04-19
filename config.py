# config.py

# Estados alvo (ES = 32, PR = 41)
ESTADOS_ALVO = ['32', '41']

# Anos alvo
ANOS = ['2023', '2024', '2025']

# Diretório para salvar os arquivos ZIP e banco
DIRETORIO_DESTINO = "banco_pnadc_pr_es"

# Nome do banco SQLite
DB_PATH = "pnadc_pr_es.db"

# Layout fornecido pelo professor
LAYOUT_PNADC = [
    ("Ano", 4), ("Trimestre", 1), ("UF", 2), ("Capital", 2), ("RM_RIDE", 2),
    ("UPA", 9), ("Estrato", 7), ("V1008", 2), ("V1014", 2), ("V1016", 1),
    ("V1022", 1), ("V1023", 1), ("V1027", 15), ("V1028", 15), ("V1029", 9),
    ("V1033", 9), ("posest", 3), ("posest_sxi", 3), ("V2001", 2), ("V2007", 1),
    ("V2009", 3), ("V2010", 1), ("V3009A", 2), ("V3014", 1), ("V4002", 1),
    ("V4012", 1), ("V4013", 5), ("V40132A", 1), ("V4015", 1), ("V40151", 1),
    ("V401511", 1), ("V401512", 2), ("V4016", 1), ("V40161", 1), ("V40162", 2),
    ("V40163", 2), ("V4017", 1), ("V40171", 1), ("V401711", 1), ("V4018", 1),
    ("V40181", 1), ("V40182", 2), ("V40183", 2), ("V4019", 1), ("V4020", 1),
    ("V4021", 1), ("V4022", 1), ("V4024", 1), ("V4025", 1), ("V4026", 1),
    ("V4027", 1), ("V4028", 1), ("V4029", 1), ("V4032", 1), ("V4033", 1),
    ("V40331", 1), ("V403312", 8), ("V403322", 8), ("V4034", 1), ("V403412", 8),
    ("V403422", 8), ("V4039", 3), ("V4039C", 3), ("V4043", 1), ("V4044", 5),
    ("V4045", 1), ("V4046", 1), ("V4048", 1), ("V4050", 1), ("V40501", 1),
    ("V405012", 8), ("V4051", 1), ("V40511", 1), ("V405112", 8), ("V405122", 8),
    ("V405912", 8), ("V405922", 8)
]

# Extrai nomes e larguras das colunas
COL_NOMES = [item[0] for item in LAYOUT_PNADC]
COL_LARGURAS = [item[1] for item in LAYOUT_PNADC]
