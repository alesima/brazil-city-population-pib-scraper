import pandas as pd
from sqlalchemy import Sequence
from .models import Municipio


def convert_to_dataframe(cities: Sequence[Municipio]):
    if cities:
        df = pd.DataFrame([city.__dict__ for city in cities])
        if '_sa_instance_state' in df.columns:
            df = df.drop(columns='_sa_instance_state')
        return df
    return None
