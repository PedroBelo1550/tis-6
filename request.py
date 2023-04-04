# Trabalho de LAB 6 
# Sprint 1

import requests
import pandas as pd
from dateutil import parser


api_token = "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"
headers = {'Authorization': 'token %s' % api_token}



def run_query(query): # Função de chamada a api
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.text, query))


# Query GraphQl 
query = """
{
  search(query: "language:Java stars:>100", type: REPOSITORY, first: 10, after: null) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        createdAt
        nameWithOwner
        releases(first: 1) {
          totalCount
        }
        stargazers {
            totalCount
          }
        url
      }
    }
  }
}
"""


end_cursor = '';

i = 0 

while(i < 100):
  
  if i == 0:
     result = run_query(query)
  else:
     result = run_query(query.replace("null", '"'  + end_cursor + '"' ))
  
  end_cursor = result['data']['search']['pageInfo']['endCursor']
  
  #Preenche o cabeçalho do CSV
  df = pd.DataFrame(columns=['createdAt',
                     'nameWithOwner',
                     'releases',
                     'stargazers',
                     'url',
                     'processado'])

  if i == 0: 
    df.to_csv('file.csv', mode='a', index=False, header=True)

  for d in result['data']['search']['nodes']:
     
     #Escreve o JSON
     data = {"createdAt" :  parser.parse(d['createdAt']).strftime("%d/%m/%Y"),
         "nameWithOwner" : d['nameWithOwner'],
         "releases" : d['releases']['totalCount'],
         "stargazers" : d['stargazers']['totalCount'],
         "url" : d['url'],
         "processado" : False}
     
     df = pd.DataFrame(data, index=[0])
    
     df.to_csv('file.csv', mode='a', index=False, header=False)

  i += 1
  print("Execução nº {}".format(i))

print('finalizou')
