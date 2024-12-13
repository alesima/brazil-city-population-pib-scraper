class Filter:
    def apply_filters(self, df, pop_min, pop_max, pib_min, pib_max, cicc=False, gcm=False, samu=False):
        return df[
            (df['populacao'] >= pop_min) & (df['populacao'] <= pop_max) &
            (df['pib_per_capita'] >= pib_min) & (df['pib_per_capita'] <= pib_max) &
            (df['possui_cicc'] == 'Sim' if cicc else True) &
            (df['possui_gcm'] == 'Sim' if gcm else True) &
            (df['possui_samu'] == 'Sim' if samu else True)
        ]
