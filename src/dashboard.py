import streamlit as st
import plotly.express as px
from .database_manager import DatabaseManager as Database
from .data_processor import convert_to_dataframe


class Visualization:
    def plot_pib_per_capita(self, df):
        return px.bar(df, x='nome', y='pib_per_capita', title='PIB Per Capita por Município')

    def plot_population(self, df):
        return px.bar(df, x='nome', y='populacao', title='População por Município')


class Filter:
    def apply_filters(self, df, query, estado, pop_min, pop_max, pib_min, pib_max, cicc=False, gcm=False, samu=False):
        filtered_df = df[
            (df['populacao'] >= pop_min) & (df['populacao'] <= pop_max) &
            (df['pib_per_capita'] >= pib_min) & (df['pib_per_capita'] <= pib_max) &
            (df['possui_cicc'] == 'Sim' if cicc else True) &
            (df['possui_gcm'] == 'Sim' if gcm else True) &
            (df['possui_samu'] == 'Sim' if samu else True)
        ]

        if query:
            filtered_df = filtered_df[filtered_df['nome'].str.contains(
                query, case=False)]

        if estado:
            filtered_df = filtered_df[filtered_df['estado'].isin(estado)]

        return filtered_df


class Sidebar:
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj

    def apply_filters(self, df):
        st.sidebar.title("Filtros")
        query = st.sidebar.text_input("Buscar por nome do município", "")
        estado = st.sidebar.multiselect(
            "Selecione o(s) Estado(s)",
            df['estado'].unique()
        )
        pop_min, pop_max = st.sidebar.slider("População", int(df['populacao'].min()), int(
            df['populacao'].max()), (int(df['populacao'].min()), int(df['populacao'].max())))
        pib_min, pib_max = st.sidebar.slider("PIB Per Capita", float(df['pib_per_capita'].min()), float(
            df['pib_per_capita'].max()), (float(df['pib_per_capita'].min()), float(df['pib_per_capita'].max())))
        cicc = st.sidebar.checkbox('Possui CICC', False)
        gcm = st.sidebar.checkbox('Possui GCM', False)
        samu = st.sidebar.checkbox('Possui SAMU', False)

        return self.filter_obj.apply_filters(df, query, estado, pop_min, pop_max, pib_min, pib_max, cicc, gcm, samu)


class Comparison:
    def __init__(self, viz_obj):
        self.viz_obj = viz_obj

    def display(self, filtered_df):
        selected_cities = st.multiselect(
            'Selecione municípios para comparar:', filtered_df['nome'].unique())
        if selected_cities:
            comparison_df = filtered_df[filtered_df['nome'].isin(
                selected_cities)]
            st.dataframe(comparison_df)

            # Display charts
            st.plotly_chart(self.viz_obj.plot_pib_per_capita(comparison_df))
            st.plotly_chart(self.viz_obj.plot_population(comparison_df))


class Dashboard:
    def __init__(self):
        self.db = Database(db_url='sqlite+aiosqlite:///municipios.db')
        self.filter = Filter()
        self.viz = Visualization()
        self.sidebar = Sidebar(self.filter)
        self.comparison = Comparison(self.viz)

    async def run(self):
        st.title("Municípios Brasileiros")

        await self.db.initialize()

        cities = await self.db.get_all_cities()

        df = convert_to_dataframe(cities)

        await self.db.close()

        # Define the order of columns and remove the 'id' column
        column_order = ['nome', 'estado', 'populacao',
                        'pib_per_capita', 'possui_cicc', 'possui_gcm', 'possui_samu']
        df = df.reindex(columns=column_order)

        filtered_df = self.sidebar.apply_filters(df)

        st.write(filtered_df)

        self.comparison.display(filtered_df)
