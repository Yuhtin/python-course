import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Carregando o dataset
df = pd.read_csv('data.csv')
print(df.head())

# Criando coluna chamada 'overweight' que será 1 se o paciente estiver com sobrepeso e 0 caso contrário
df['overweight'] = ((df['weight'] / ((df['height'] / 100) ** 2)) > 25).astype(int)
print(df.head())

# Normalizando os dados de cholesterol e gluc 
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# Função para plotar o gráfico de barras
def draw_cat_plot():
    # Desmembrando o dataframe em várias colunas
    df_melted = pd.melt(
        df,
        id_vars=['cardio'],  
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']  
    )

    # Contando o número de vezes que cada valor aparece
    df_melted = df_melted.value_counts(['cardio', 'variable', 'value']).reset_index(name='total')

    order = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']

    # Plotando o gráfico de barras
    graph_plot = sns.catplot(
        x='variable', y='total', hue='value', col='cardio',
        height=5, aspect=1, data=df_melted, kind='bar', order=order
    )

    # Salvando o gráfico no arquivo catplot.png
    graph_plot.figure.savefig('CatPlot Gerado.png')
    return graph_plot.figure

# Função para plotar o heatmap
def draw_heat_map():
    # Modificando o dataframe para remover outliers
    # Filtrando apenas por Altura e Peso que estão dentro do intervalo de 2.5% a 97.5% inter-quartil
    # Filtrando apenas por pressão arterial sistólica (ap_hi) que é maior que a diastólica (ap_lo)
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) &  
        (df['weight'] >= df['weight'].quantile(0.025)) &  
        (df['weight'] <= df['weight'].quantile(0.975))   
    ]

    # Fazendo o mapa de correlação
    corr = df_heat.corr()

    # Ocultando a metade superior do mapa de correlação evitando repetição de informações
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Criando o gráfico
    figure, ax = plt.subplots(figsize=(12, 12))

    # Plotando o mapa de calor
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    figure.savefig('HeatMap Gerado.png')
    return figure
