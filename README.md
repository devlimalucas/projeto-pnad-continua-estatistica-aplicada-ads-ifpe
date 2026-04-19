# 📊 Projeto PNAD Contínua – ES e PR <br>

Este projeto automatiza o download, processamento e armazenamento dos microdados da PNAD Contínua (IBGE) para os estados do Espírito Santo (ES) e Paraná (PR). <br><br>

## 📌 Funcionalidades <br>

- Conexão ao FTP do IBGE para baixar arquivos ZIP de microdados <br>
- Processamento dos arquivos TXT contidos nos ZIPs usando pandas.read_fwf com layout fixo <br>
- Filtragem dos dados apenas para os estados ES (32) e PR (41) <br>
- Armazenamento em dois bancos SQLite distintos: pnadc_es.db e pnadc_pr.db <br>
- Exportação automática de dois arquivos CSV: pnadc_es.csv e pnadc_pr.csv <br>
- Relatório de valores nulos por coluna durante o processamento <br>
- Resumo dos dados por ano e trimestre diretamente no terminal <br>
- Lógica de execução: <br>
  - Primeira execução: baixa todos os arquivos <br>
  - Execuções seguintes: reaproveita os arquivos locais e baixa apenas os que faltam <br>
- Reconexão automática ao FTP em caso de falha (até 3 tentativas) <br>
- Validação de integridade dos arquivos ZIP baixados <br><br>

## ⚙️ Estrutura do Projeto <br>

- config.py → Configurações de anos, estados e layout das colunas <br>
- ftp_utils.py → Funções de conexão e download via FTP <br>
- processing.py → Processa os arquivos TXT e gera DataFrames filtrados <br>
- database.py → Salva dados em bancos separados e exporta CSVs/resumos <br>
- main.py → Orquestra todo o fluxo (FTP, download, processamento, banco, CSV) <br><br>

## 🖥️ Tecnologias necessárias <br>

- Python 3.10+ (testado em Python 3.13) <br>
- pip (gerenciador de pacotes do Python) <br>
- Bibliotecas Python: pandas, sqlite3 (já incluso no Python), ftplib (já incluso no Python), os e zipfile (já inclusos no Python) <br>
- Opcional: Git para clonar o repositório, Virtualenv/venv para criar ambiente isolado <br><br>

## 🚀 Como rodar <br>

1. Clone este repositório: <br><br>
   git clone (url-do-repo) <br>
   cd projeto-pnad-continua <br><br>

2. Instale as dependências (se necessário, crie um ambiente virtual): <br><br>
   pip install -r requirements.txt <br><br>

3. Execute o script principal: <br><br>
   python main.py <br><br>

> Não é necessário configurar nada além disso. O programa já está pronto para rodar e gerar os bancos e CSVs automaticamente. <br><br>

## 📂 Estrutura de saída <br>

- Diretório de destino: contém os arquivos ZIP baixados <br>
- Bancos SQLite: armazenam os dados filtrados por estado <br>
- CSVs: exportação final para análise <br>
- Resumo: exibido no terminal, mostrando registros por ano e trimestre <br><br>

## 🛠️ Observações <br>

- Se a conexão FTP falhar, o sistema tenta reconectar até 3 vezes <br>
- Se não conseguir, usa os arquivos locais já baixados <br>
- Valores nulos são preservados no banco e relatados no terminal <br>
- Arquivos inválidos ou corrompidos são descartados e baixados novamente <br>
- O programa garante que todos os 4 trimestres de cada ano sejam processados <br><br>

## 🔄 Fluxo de execução <br>

FTP IBGE → Download ZIP → Processamento TXT → Filtragem ES/PR → Bancos SQLite → Exportação CSV → Resumo no terminal <br>
