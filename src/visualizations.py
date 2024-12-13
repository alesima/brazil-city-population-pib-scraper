import plotly.express as px


class Visualization:
    def plot_pib_per_capita(self, df):
        return px.bar(df, x='nome', y='pib_per_capita', title='PIB Per Capita por Município')

    def plot_estimated_revenue(self, df):
        return px.bar(df, x='nome', y='receita_estimada', title='Receita Estimada por Município')
