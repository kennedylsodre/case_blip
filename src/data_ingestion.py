#%%
import pandas as pd 
import pandas_gbq as gbq
import os 
from  tqdm import tqdm
#%%
def read_send_big_query(path_data, project_id, schema):
    """
    Lê arquivos CSV de um diretório, converte a coluna 'StorageDate' para datetime com UTC,
    e envia os dados para tabelas no BigQuery.

    Para cada arquivo `.csv` encontrado no diretório especificado, esta função:
      - Lê o arquivo como DataFrame pandas (usando delimitador ';'),
      - Converte a coluna 'StorageDate' para datetime com timezone UTC,
      - Gera um nome de tabela com base no nome do arquivo (removendo 'DadosBrutos' e '.csv'),
      - Envia os dados para o BigQuery usando `pandas_gbq.to_gbq`, substituindo a tabela se já existir.

    Args:
        path_data (str): Caminho para o diretório onde estão os arquivos CSV.
        project_id (str): ID do projeto no Google Cloud.
        schema (str): Nome do dataset (esquema) no BigQuery onde as tabelas serão criadas.
    """

    for file in tqdm(os.listdir(path_data)):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(path_data, file), delimiter=';')
            df['StorageDate'] = pd.to_datetime(df['StorageDate'], utc=True)
            tabela = file.replace('DadosBrutos', '').replace('.csv', '')
            gbq.to_gbq(df, f'{schema}.{tabela}', project_id=project_id, if_exists='replace')


# %%
path_data = '../data'
project_id = 'carna-belo'
schema = 'carna_belo_bot'

read_send_big_query(path_data,project_id,schema)
# %%
