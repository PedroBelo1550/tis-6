import pandas as pd
from git.repo.base import Repo
import shutil
import os

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


               # O código do designate deve ser chamado aqui....

                # delete a pasta arquivos
                # shutil.rmtree('arquivos')
                #os.mkdir('arquivos')

                

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
        df.loc[df['name'] == d[0], 'processado'] = True
        df.to_csv('repositorios.csv', header=[
                                'name','owner','url','totalPullRequests','closed','merged','processado'], index=False, mode='w')

        print('Url concluída')
        break

    i += 1 

#Exclui o diretório
#shutil.rmtree('repositorios')
#os.mkdir('repositorios')

print('Execução do script concluída')