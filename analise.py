import time
import pandas as pd
from git.repo.base import Repo
import shutil
import os
import subprocess
from arquivos import Arquivos
import sqlalchemy
import stat
import platform

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def move_to_trash(file_path):

    while True:
        try:
            system = platform.system()
            if system == 'Windows':
                shutil.rmtree(file_path, onerror=remove_readonly)
            else: 
                shutil.rmtree(file_path)
            
            return True
        except Exception as err:
            print(f'Error ao excluir o arquivo: {err}')
            print('Sleeping for 10 seconds...')
            time.sleep(10)

        


#Banco de dados, conexao
database_username = 'admintis'
database_password = 'Tisseis6'
database_ip       = 'tis6.mysql.database.azure.com'
database_name     = 'tis6'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
conn = database_connection.connect()

df = pd.read_csv('repositorios.csv')

if os.path.isdir('atual'):
    move_to_trash('atual')

if os.path.isdir('output'):
    move_to_trash('output')
    
os.mkdir('atual')
os.mkdir('output')

i = 0

for d in df.values:

    conn = database_connection.connect()

    if(d[6] == False):

        print('Clonando respositório {}'.format(d[1]))
        #Exclui o diretório
        move_to_trash('repositorios')
        #Cria o diretório
        os.mkdir('repositorios')
        #Clona o repositório
        Repo.clone_from(d[2], 'repositorios')

        stmt = sqlalchemy.text("CALL get_commit(:param1, :param2)")

        #Passa como parâmetro o owner e o name do repositório.
        # chamar o stored procedure e carregar o resultado em um DataFrame
        commits = pd.read_sql(stmt, con=conn, params={"param1": d[1], "param2": d[0]})


        tamanho_df = len(commits)
        print(f"tamanho df {tamanho_df}")

        i = 0

        pull_request = None

        for c in commits.values:

            if(c[5] == 'False'):
                arquivo = Arquivos(c[3])

                if(i == 0):
                    pull_request = c[2]

                if(pull_request != c[2]):
                    print(f'acabou um pull request do repositorio {d[0]}, percentual executado:  {(i / tamanho_df * 100)}')
                # break

                if(c[4] == 'MERGED'):
                    arquivo.list_arquivos()
                else:
                    arquivo.get_arquivos_closed(c[0], c[1], c[2], i)

            
                input_path = './atual' 
                output_path = './output/'

                if os.listdir(input_path):
                    command = f'java -jar DesigniteJava.jar -i {input_path} -o {output_path}'
                    result = subprocess.run(command, shell=True, check=True)

                    # Lê o arquivo CSV usando o pandas
                    csv_path = output_path + 'ImplementationSmells.csv'
                    cdsm = pd.read_csv(csv_path, encoding='ISO-8859-1')
                    cdsm = cdsm.drop(['Project Name', 'Package Name', 'Method Name', 'Cause of the Smell', 'Method start line no'], axis=1)
                    cdsm['commit'] = c[3].split('/')[-1]
                    cdsm['pull_number'] = c[2]
                    cdsm['name'] = d[0]
                    cdsm['owner'] = d[1]
                    cdsm['status'] = c[4]
                    cdsm = cdsm.rename(columns={'Type Name': 'file'})
                    cdsm['file'] = cdsm['file'] + '.atual' 
                    file_exists = os.path.isfile('code_smells.csv') # Verifica se o arquivo já existe no diretório

                    # Inserindo os dados na tabela do banco de dados
                    cdsm.to_sql(name='code_smells', con=database_connection, if_exists='append', index=False)                    
                    
                    # DESIGNITE END
                    move_to_trash('atual')
                    os.mkdir('atual')

                with database_connection.connect() as conn:
                    stmt = sqlalchemy.text("update commit set processado = 'True' where name = :name and owner = :owner and commitUrl = :url")
                    result = conn.execute(stmt, {'name' : d[0], 'owner': d[1],'url': c[3]})
                    conn.commit()

            i += 1

        #Atualiza o arquivo para controlar a coleta. 
        print('Salvando no repositorio.')
        df.loc[df['name'] == d[0], 'processado'] = True
        df.to_csv('repositorios.csv', header=True, index=False, mode='w')
        print(f'Repositório {d[0]} processado, dormindo por 5 segundos...')
        time.sleep(5)

    i += 1 

print('Execução do script concluída')