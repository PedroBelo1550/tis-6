
import io
import subprocess
import zipfile
import requests
class Arquivos:


    def __init__(self, url_commit: str) -> None:
        self.repo_path = "./repositorios"
        self.hash = url_commit.split("/")[-1]


    def list_arquivos(self):

        # Executa o comando e captura a saída

        file_list = []
        output = None

        try: 
            output = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", self.hash], cwd=self.repo_path)
        
            # Decodifica a saída em uma string e divide os nomes de arquivo em uma lista
            file_list = output.decode("utf-8").splitlines()

        except Exception:
                print('Erro')

      
        # Itera pelos arquivos listados
        for file in file_list:

            if(file[-5:] == '.java'):

                try: 
                    #Atual
                    command = f"git show {self.hash}:{file}"
            
                    result = subprocess.check_output(command, cwd=self.repo_path, shell=True)

                    # salva o resultado em um arquivo .java
                    with open("./arquivos/" + file.split("/")[-1][:-5] + "_atual.java", 'w') as fi:
                        fi.write(result.decode("utf-8"))

                    #Anterior
                    command = f"git show {self.hash}~1:{file}"

                    result = subprocess.check_output(command, cwd=self.repo_path, shell=True)

                    # salva o resultado em um arquivo .java
                    with open("./arquivos/" + file.split("/")[-1][:-5] + "_anterior.java", 'w') as fi:
                        fi.write(result.decode("utf-8"))

                    
                except Exception:
                    print('Erro')


    def list_arquivo_closed(self, name, owner):

        access_token = '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'

        # faça uma solicitação GET para a URL da API do GitHub correspondente ao commit desejado
        url = f'https://api.github.com/repos/{owner}/{name}/commits/{self.hash}'
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(url, headers=headers)

        # analise a resposta JSON para extrair a lista de arquivos modificados
        commit_data = response.json()
        print(commit_data)
        modified_files = commit_data['files']

        # imprima a lista de arquivos modificados
        for file in modified_files:
            print(file['filename'])



