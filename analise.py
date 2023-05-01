import pandas as pd
from git.repo.base import Repo
import shutil
import os
import subprocess

from arquivos import Arquivos

df = pd.read_csv('repositorios.csv')

i = 0

for d in df.values:

    if(d[6] == False):

        print('Clonando respositório {}'.format(d[1]))
        #Exclui o diretório
        shutil.rmtree('repositorios')
        #Cria o diretório
        os.mkdir('repositorios')
        #Clona o repositório
        Repo.clone_from(d[2], 'repositorios')

        commits = pd.read_csv('files.csv')

        i = 0

        pull_request = None

        for c in commits.values:

            if(c[5] == False):
                arquivo = Arquivos(c[3])

                if(i == 0):
                    pull_request = c[2]

                if(pull_request != c[2]):
                    print('acabou um pull request')
                # break

                if(c[4] == 'MERGED'):
                    arquivo.list_arquivos()
                else:
                    arquivo.get_arquivos_closed(c[0], c[1], c[2])

                # DESIGNITE INI
                # Executa o comando 
                diretorios = ['atual', 'anterior']
                for n in diretorios:
                    print(n)
                    input_path = './' +  n
                    output_path = './output/'
                    command = f'java -jar DesigniteJava.jar -i {input_path} -o {output_path}'
                    result = subprocess.run(command, shell=True, check=True)

                    # Lê o arquivo CSV usando o pandas
                    csv_path = output_path + 'ImplementationSmells.csv'
                    cdsm = pd.read_csv(csv_path)
                    cdsm = cdsm.drop(['Project Name', 'Package Name', 'Method Name', 'Cause of the Smell', 'Method start line no'], axis=1)
                    cdsm['commit'] = c[3].split('/')[-1]
                    cdsm['pull_number'] = c[2]
                    cdsm['name'] = d[0]
                    cdsm['owner'] = d[1]
                    cdsm['status'] = c[4]
                    cdsm = cdsm.rename(columns={'Type Name': 'file'})
                    cdsm['file'] = cdsm['file'] + '.' + n

                    file_exists = os.path.isfile('code_smells.csv') # Verifica se o arquivo já existe no diretório

                    if not file_exists: # Se o arquivo não existe, escreve o cabeçalho
                        cdsm.to_csv('code_smells.csv', sep=',', index=False, mode='w')
                        print('vazio')
                    else: # Se o arquivo já existe, adiciona apenas os dados
                        cdsm.to_csv('code_smells.csv', sep=',', index=False, mode='a', header=False)
                        print('append')
                        
                    if(n=='anterior'):
                        break
                
                # DESIGNITE END
                shutil.rmtree('atual')
                os.mkdir('atual')

                i += 1

        #Atualiza o arquivo para controlar a coleta. 
        print('Salvando no repositorio.')

        df.loc[df['name'] == d[0], 'processado'] = True
        df.to_csv('repositorios.csv', header=True, index=False, mode='w')

        commits.loc[df['commitUrl'].split("/")[-1] == d[3], 'processado'] = True
        commits.to_csv('files.csv', header=True, index=False, mode='w')

        print('Url concluída')
        break

    i += 1 

#Exclui o diretório
#shutil.rmtree('repositorios')
#os.mkdir('repositorios')

print('Execução do script concluída')