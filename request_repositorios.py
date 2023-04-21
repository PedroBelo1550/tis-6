# Trabalho de LAB 6 
# Sprint 1

import requests
import pandas as pd
from dateutil import parser


api_token = "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"
headers = {'Authorization': 'token %s' % api_token}
nome_arquivo = "repositorios.csv"


def run_query(query): # Função de chamada a api
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.text, query))


# Query GraphQl 
query = """
{
  search(
    query: "language:Java stars:>100"
    type: REPOSITORY
    first: 10
    after: null
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        name
        owner {
          login
        }
        url
        pullRequests {
          totalCount
        }
        closed: pullRequests(states: CLOSED) {
          totalCount
        }
        merged: pullRequests(states: MERGED) {
          totalCount
        }
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
     result = run_query(query.replace("null", '"'  + end_cursor + '"' ))
  
  end_cursor = result['data']['search']['pageInfo']['endCursor']
  
  #Preenche o cabeçalho do CSV
  df = pd.DataFrame(columns=[
                     'name',
                     'owner',
                     'url',
                     'totalPullRequests',
                     'closed',
                     'merged',
                     'processado'])

  if i == 0: 
    df.to_csv(nome_arquivo, mode='a', index=False, header=True)

  for d in result['data']['search']['nodes']:
     
     #Escreve o JSON
     data = {
         "name" : d['name'],
         "owner" : d['owner']['login'],
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
