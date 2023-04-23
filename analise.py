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

            arquivo = Arquivos(c[3])

           
            if(i == 0):
                pull_request = c[2]

            if(pull_request != c[2]):
                print('acabou um pull request')
                break


            if(c[4] == 'MERGED'):
                arquivo.list_arquivos()
            else:
                arquivo.get_arquivos_closed(c[0], c[1], c[2])


            # DESIGNITE INI
            # Executa o comando 
            diretorios = ['atual', 'anterior']
            for n in diretorios:
                print(n)
                input_path = '/Users/pedrobarcelos/tis-6/' +  n
                output_path = '/Users/pedrobarcelos/tis-6/output/'
                command = f'java -jar DesigniteJava.jar -i {input_path} -o {output_path}'
                subprocess.run(command, shell=True, check=True)

                # Lê o arquivo CSV usando o pandas
                csv_path = output_path + 'ImplementationSmells.csv'
                cdsm = pd.read_csv(csv_path)
                cdsm = cdsm.drop(['Project Name', 'Package Name', 'Method Name', 'Cause of the Smell', 'Method start line no'], axis=1)
                cdsm['commit'] = c[3].split('/')[-1]
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

                # delete a pasta arquivos
            shutil.rmtree('atual')
            shutil.rmtree('anterior')
            os.mkdir('atual')
            os.mkdir('anterior')

                

            i += 1

            # if(i == 10):
            #     break
            


        #Executa o CK
        #os.system('java -jar ck.jar ./repositorios false 0 False ./ck_result/')
        #Coleta o resultado. 
        #result = pd.read_csv('./ck_result/class.csv')

        # #Monta o arquivo de resultado
        # data = {"createdAt" :  d[0],
        #  "releases" : d[2],
        #  "stargazers" : d[3],
        #  "url" : d[4],
        #  "cbo" : result['cbo'].median(),
        #  "dit": result['dit'].max(),
        #  "lcom": result['lcom'].median(),
        #  "loc": result['loc'].sum()}

        #Atualiza o arquivo para controlar a coleta. 
        print('Salvando no repositorio.')
        ##df.loc[df['name'] == d[0], 'processado'] = True
        ##df.to_csv('repositorios.csv', header=[
         ##                       'name','owner','url','totalPullRequests','closed','merged','processado'], index=False, mode='w')

        print('Url concluída')
        break

    i += 1 

#Exclui o diretório
#shutil.rmtree('repositorios')
#os.mkdir('repositorios')

print('Execução do script concluída')