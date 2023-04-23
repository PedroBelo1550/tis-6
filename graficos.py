import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('pull_requests.csv')

#Altere aqui as variável desejadas. 
x = 'state' #Eixo X 
y = 'bodyText' #Eixo Y

#Tratamento de outlier
media = df[y].mean()
desvioPadrao = df[y].std()
limite_superior = media + desvioPadrao;
limite_inferior = media - desvioPadrao;

titulo = 'Relação entre ' + x + ' e ' + y 
plt.scatter(x=x, y=y, data=df[(df[y] <= limite_superior) & (df[y] >= limite_inferior)])

df[x] = df[x].map({'MERGED': 1, 'CLOSED': 0})
r = df[[x, y]].corr(method='spearman')
r = r['bodyText'][0]
print(r)
plt.legend(title=f'Correlação Spearman (r) = {r:.2f}', loc='upper center', bbox_to_anchor=(0.5, -0.15))

plt.xlabel(x)
plt.ylabel(y)
plt.title(titulo)
plt.show()


