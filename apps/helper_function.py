import pandas as pd
import streamlit as st


def get_gdp_ranking(df, option_country):
    years = [1960, 1970, 1980, 1990, 2000, 2010, 2019]
    rankings = []
    for year in years:
        r = df[df['year'] == year] \
                .sort_values(by='value', ascending=False).reset_index()
        idx = r.index[r['cname'] == option_country][0]
        rankings.append(idx + 1)
    return pd.DataFrame({'Year': years,
                         'Ranking': rankings})


def custom_legend_name(fig, new_names):
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name


def no_data():
    st.markdown("There is no data available for this \
                 country :disappointed:")
