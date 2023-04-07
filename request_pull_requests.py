# Trabalho de LAB 6 
# Sprint 1

import requests
import pandas as pd
from dateutil import parser


api_token = "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"
headers = {'Authorization': 'token %s' % api_token}
nome_arquivo = "resultados.csv"


def run_query(query): # Função de chamada a api
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.text, query))


# Query GraphQl 
query = """
query pullResquest {
  repository(name: "java-design-patterns", owner: "iluwatar") {
    pullRequests(last: 10, after: null) {
      nodes {
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
        files(first: 100, after: null) {
          nodes {
            path
            changeType
            additions
            deletions
          }
         cursorFile: pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
     cursorRepo: pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

end_cursor = '';

i = 0 

while(i < 10):
  
  if i == 0:
     result = run_query(query)
  else:
     result = run_query(query.replace("pullRequests(last: 10, after: null)", '" pullRequests(last: 10, after: '  + end_cursor + ')"' ))
  
  end_cursor = result['data']['search']['pageInfo']['endCursor']
  
  #Preenche o cabeçalho do CSV
  df = pd.DataFrame(columns=[
                     'nameWithOwner',
                     'url',
                     'totalPullRequests',
                     'closed',
                     'merged',
                     'processado'])

  if i == 0: 
    df.to_csv(nome_arquivo, mode='a', index=False, header=True)

  for d in result['data']['repository']['pullRequests']['nodes']:
     
     #Escreve o JSON
     data = {
         "nameWithOwner" : d['nameWithOwner'],
         "url" : d['url'],
         "totalPullRequests" : d['pullRequests']['totalCount'],
         "closed": d['closed']['totalCount'],
         "merged": d['merged']['totalCount'],
         "processado" : False}
     
     df = pd.DataFrame(data, index=[0])
    
     df.to_csv(nome_arquivo, mode='a', index=False, header=False)

  i += 1
  print("Execução nº {}".format(i))

print('finalizou')
