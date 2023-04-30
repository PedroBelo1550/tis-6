import pandas as pd
import matplotlib.pyplot as plt

arquivo = 'code_smells.csv'

df = pd.read_csv(arquivo)

# agrupar por bads_smells e status e contar o número de ocorrências de cada grupo
groups = df.groupby(['Implementation Smell', 'status']).size().reset_index(name='count')

# pivotar a tabela para ter bads_smells como índice e status como colunas
pivot_table = pd.pivot_table(groups, values='count', index='Implementation Smell', columns='status', fill_value=0)

# plotar o gráfico de barras
pivot_table.plot.bar()

# adicionar rótulos e título
plt.xlabel('Status')
plt.ylabel('Número de Bad Smells')
plt.title('Contagem de Bad Smells por Status')

# mostrar o gráfico
plt.show()




