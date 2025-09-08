
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Leitura do arquivo CSV
df = pd.read_csv('data.csv', parse_dates=['date'], index_col='date')

# Remoção de outliers
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]

def draw_line_plot():
    # Criação do gráfico de linha
    figure, axes = plt.subplots(figsize=(15, 5))
    
    axes.plot(df.index, df['value'], color='red', linewidth=1)
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    
    # Salvando o gráfico
    figure.savefig('Gráfico de Linha.png')
    return figure

def draw_bar_plot():
    # Criação do dataframe separado para o gráfico de barras
    # Criando colunas para ano, mês e nome do mês
    df_barplot = df.copy()
    
    df_barplot['year'] = df_barplot.index.year
    df_barplot['month'] = df_barplot.index.month
    df_barplot['month_name'] = df_barplot.index.strftime('%B')
   
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Ordenando os meses
    df_barplot['month_name'] = pd.Categorical(df_barplot['month_name'], categories=months_order, ordered=True)
    
    # Agrupando por ano e mês e calculando a média
    df_barplot = df_barplot.groupby(['year', 'month_name'])['value'].mean().unstack()

    # Draw bar plot
    figure = plt.figure(figsize=(15, 10))
    chart_axes = df_barplot.plot(kind='bar', ax=plt.gca())
    
    chart_axes.set_xlabel('Years')
    chart_axes.set_ylabel('Average Page Views')
    chart_axes.legend(title='Months')
    
    # Salvando o gráfico
    figure.savefig('Grafico de Barras.png')
    return figure

def draw_box_plot():
    # Preparando o dataframe para o gráfico de caixas
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # Criando colunas para ano e mês
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Criando os gráficos de caixas
    figure, axes = plt.subplots(1, 2, figsize=(20, 7))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Salvando o gráfico
    figure.savefig('Gráfico de BoxPlot.png')
    return figure
