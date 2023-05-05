
import subprocess
import requests
from token_git import TokenGit
class Arquivos:


    def __init__(self, url_commit: str) -> None:
        self.repo_path = "./repositorios"
        self.hash = url_commit.split("/")[-1]
        self.token = TokenGit()


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
                    with open("./atual/" + file.split("/")[-1][:-5] + "_atual.java", 'w') as fi:
                        fi.write(result.decode("utf-8"))
    
                except Exception:
                    print('Erro')

    def list_arquivos_closed(self, numero_pull, name, owner, i):

        access_token = self.token.get_Token(i)

        query = """
        query MyQuery {
        repository(name: "%s", owner: "%s") {
            pullRequest(number: %d) {
            files(first: 100) {
                nodes {
                path
                }
            }
            }
        }
        }
        """ % (name, owner, numero_pull)

        data = {'query': query}
        headers = {'Authorization': f'token {access_token}'}

        try:
            response = requests.post('https://api.github.com/graphql', headers=headers, json=data)

            if(response.status_code != 200):
                print(f'Error: {response.text}')

        except Exception as err:
          print(f'Error: {err}')

        return response.json()

    def get_arquivos_closed(self, name, owner, num_pull, i):

        df = self.list_arquivos_closed(num_pull,name,owner, i)

        df = df['data']['repository']['pullRequest']['files']['nodes']

        for a in df:

            if(a['path'][-5:] == '.java'):

                path = a['path']

                # faça uma solicitação GET para a URL da API do GitHub correspondente ao commit desejado
                url = f'https://raw.githubusercontent.com/{owner}/{name}/{self.hash}/{path}'
                response = requests.get(url)

                # analise a resposta JSON para extrair a lista de arquivos modificados
                commit_data = response.text

                # salva o resultado em um arquivo .java
                with open("./atual/" + path.split("/")[-1][:-5] + "_atual.java", 'w', encoding='utf-8') as fi:
                    fi.write(commit_data)

       



