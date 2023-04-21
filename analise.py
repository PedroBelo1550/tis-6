import pandas as pd
from git.repo.base import Repo
import shutil
import os

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
shutil.rmtree('repositorios')

print('Execução do script concluída')