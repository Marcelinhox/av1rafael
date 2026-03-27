import pandas as pd

arquivo = 'dados/faturas.xlsx'

df = pd.read_excel(arquivo)

for index, row in df.iterrows():
    print(row['cpf'], row['valor'])