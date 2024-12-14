import pandas as pd
from sqlalchemy import Sequence
from .models import Municipio


def convert_to_dataframe(cities: Sequence[Municipio]):
    if cities:
        df = pd.DataFrame([city.__dict__ for city in cities])
        if '_sa_instance_state' in df.columns:
            df = df.drop(columns='_sa_instance_state')

        # Map the values of 'possui_cicc', 'possui_gcm', and 'possui_samu'
        df['possui_cicc'] = df['possui_cicc'].map({1: 'Sim', 0: 'Não'})
        df['possui_gcm'] = df['possui_gcm'].map({1: 'Sim', 0: 'Não'})
        df['possui_samu'] = df['possui_samu'].map({1: 'Sim', 0: 'Não'})

        return df
    return None
