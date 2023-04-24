# Trabalho de LAB 6
# Sprint 1

import requests
import pandas as pd
import time

nome_arq_pull = "pull_requests.csv"
nome_arq_files = "files.csv"

# Alterna o token de acesso


def change_token(count):
    api_token_pedro = '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'
    api_token_y = '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'

    if (count % 2 == 0):
        return api_token_pedro
    else:
        return api_token_y


def run_query(query):  # Função de chamada a api

    while True:

      try:
        headers = {'Authorization': 'token %s' % change_token(i)}
        request = requests.post('https://api.github.com/graphql',
                                json={'query': query}, headers=headers)
        if request.status_code != 200:
          print(request.json())
          print('Erro recebido. Aguardando 5 minutos...')
          time.sleep(300)  # Dorme por 5 minutos 
        else:
          print(request.status_code)
          return request.json()
      except Exception as err:
          print(f'Error: {err}')
          print(f'Sleeping for 5 minutes...')
          time.sleep(300)


def get_dados(name, owner):

    # Query GraphQl
    query = """
    query pullResquest {
      repository(name: "java-design-patterns", owner: "iluwatar") {
        pullRequests(first: 50, after: null, states: [MERGED, CLOSED]) {
          cursorPull: pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            number
            closedAt
            createdAt
            state
            author {
              login
            }
            bodyText
            changedFiles
            comments {
              totalCount
            }
            commits(first: 100) {
              nodes {
                commit {
                  commitUrl
                }
              }
            }
          }
        }
      }
    }
    """
    end_cursor = ''

    parada = pd.read_csv('cursor.csv')

    if (not parada.empty):
        if (name == parada['name'][0]):
            name = parada['name'][0]
            owner = parada['owner'][0]
            end_cursor = parada['cursor'][0]

    query = query.replace('name: "inicio", owner: "inicio"',
                          'name: "' + name + '", owner: "' + owner + '"')
    next_page = True

    i = 0

    print('Cursor inicio {}'.format(end_cursor))

    while (next_page):

        if i == 0 and end_cursor == '':
            result = run_query(query)
        else:
            result = run_query(query.replace("null", '"' + end_cursor + '"'))

        end_cursor = result['data']['repository']['pullRequests']['cursorPull']['endCursor']
        next_page = result['data']['repository']['pullRequests']['cursorPull']['hasNextPage']

        df_pull = pd.DataFrame(columns=[
            "name",
            "owner",
            "number",
            'closedAt',
            'createdAt',
            'state',
            'authorLogin',
            'bodyText',
            'changedFiles',
            'comments'])
        
        df_file = pd.DataFrame(columns=[
                      "name",
                      "owner",
                      "number",
                      'commitUrl',
                       'state',
                       'processado'])

        if i == 0:
            df_pull.to_csv(nome_arq_pull, mode='a', index=False, header=True)
            df_file.to_csv(nome_arq_files, mode='a', index=False, header=True)

        for d in result['data']['repository']['pullRequests']['nodes']:

            data_pull = {
                "name": name,
                "owner": owner,
                "number": d['number'],
                "closedAt": d['closedAt'],
                "createdAt": d['createdAt'],
                "state": d['state'],
                "authorLogin": d['author']['login'] if d['author'] is not None else 'null',
                "bodyText": len(d['bodyText']),
                "changedFiles": d['changedFiles'],
                "comments": d['comments']['totalCount']
            }

            for f in d['commits']['nodes']:

                data_file = {
                    "name": name,
                    "owner": owner,
                    "number": d['number'],
                    "commitUrl": f['commit']['commitUrl'],
                    "state": d['state'],
                    "processado": False
                   
                }

                df_file = pd.DataFrame(data_file, index=[0])
                df_file.to_csv(nome_arq_files, mode='a', index=False, header=False)

            df_pull = pd.DataFrame(data_pull, index=[0])
            df_pull.to_csv(nome_arq_pull, mode='a', index=False, header=False)

        i += 1
        print(next_page)

        print("Cursor executado {}".format(end_cursor))

        cursor = {"name": name,
                  "owner": owner,
                  "cursor": end_cursor}

        df_cursor = pd.DataFrame(cursor, index=[0])
        df_cursor.to_csv("cursor.csv")

        print("Execução nº {}".format(i))

        time.sleep(0.1)


# Itera sobre os repositórios
repositorios = pd.read_csv('repositorios.csv')
i = 0
for d in repositorios.values:
    if (d[6] == False):

        get_dados(d[0], d[1])

        try:
            print('Salvando no repositorio.')
            repositorios.loc[repositorios['name'] == d[0], 'processado'] = True
            repositorios.to_csv('repositorios.csv', header=[
                                'name', 'owner', 'url', 'processado'], index=False, mode='w')
        except Exception as e:
            print(e)

        i += 1

        print("Coletou {} repositorios".format(i))
        print('Dormindo...')
        time.sleep(60)


print('finalizou a coleta dos pull Requests')
