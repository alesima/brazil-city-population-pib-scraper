import asyncio
import streamlit as st
from .database_manager import DatabaseManager as Database
from .filters import Filter
from .visualizations import Visualization
from .data_processor import convert_to_dataframe


class Dashboard:
    def __init__(self):
        # Replace with your actual DB URL
        self.db = Database(db_url='sqlite+aiosqlite:///municipios.db')
        self.filter = Filter()
        self.viz = Visualization()
        self.df = None

    async def run(self):
        st.title("Municipal Dashboard")

        await self.db.initialize()

        cities = await self.db.get_all_cities()
        df = convert_to_dataframe(cities)

        await self.db.close()

        # Sidebar for filters
        st.sidebar.title("Filtros")
        pop_min, pop_max = st.sidebar.slider("População", int(df['populacao'].min()), int(
            df['populacao'].max()), (int(df['populacao'].min()), int(df['populacao'].max())))
        pib_min, pib_max = st.sidebar.slider("PIB Per Capita", float(df['pib_per_capita'].min()), float(
            df['pib_per_capita'].max()), (float(df['pib_per_capita'].min()), float(df['pib_per_capita'].max())))
        cicc = st.sidebar.checkbox('Possui CICC?', False)
        gcm = st.sidebar.checkbox('Possui GCM?', False)
        samu = st.sidebar.checkbox('Possui SAMU?', False)

        # Apply filters
        filtered_df = self.filter.apply_filters(
            df, pop_min, pop_max, pib_min, pib_max, cicc, gcm, samu)

        # Display filtered municipalities
        st.write("Municípios Filtrados:", filtered_df)

        # Comparison Feature
        selected_cities = st.multiselect(
            'Selecione municípios para comparar:', filtered_df['nome'].unique())
        if selected_cities:
            comparison_df = filtered_df[filtered_df['nome'].isin(
                selected_cities)]
            st.dataframe(comparison_df)

            # Display charts
            st.plotly_chart(self.viz.plot_pib_per_capita(comparison_df))
            st.plotly_chart(self.viz.plot_estimated_revenue(comparison_df))

        if st.button('Mostrar todos os dados'):
            st.dataframe(df)


if __name__ == "__main__":
    asyncio.run(Dashboard().run())
