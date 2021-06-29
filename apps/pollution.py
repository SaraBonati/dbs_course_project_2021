# Pollution section of the DBS Project dashboard
# (the multi-app framework is taken from https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import numpy as np
import os 
import plotly.express as px
from plotly.subplots import make_subplots
from apps.database_connection import DB

# directory management 
wdir           = os.getcwd()
ddir           = os.path.join(wdir,'data')
raw_data_dir   = os.path.join(ddir,'raw')
final_data_dir = os.path.join(ddir,'final')

# database class (to handle connecion to DB + execute and retrieve query results)
db = DB('dbs_project')

def get_gdp_ranking(df,option_country):
    years = [1960,1970,1980,1990,2000,2010,2019]
    rankings = []
    for year in years:
        r = df[df['Year']==year].sort_values(by='Gdp', ascending=False).reset_index()
        idx = r.index[r['Country Name']==option_country][0]
        rankings.append(idx+1)
    return  pd.DataFrame({'Year': years,
                          'Ranking':rankings})


def app():
    # import data (note: I am using the csv file to try the visualizations first, 
    # in the final app the data to be visualized will be obtained via SQL query)
    health = pd.read_csv(os.path.join(final_data_dir,'HEALTH.csv'),header=0)
    country = pd.read_csv(os.path.join(final_data_dir,'COUNTRY.csv'),header=0)
    gdp = pd.read_csv(os.path.join(final_data_dir,'GDP.csv'),header=0)

    st.title('Pollution')

    query_part_of_world = """
                          SELECT DISTINCT partofworld
                          FROM public.country;  
                          """
    
    #option_world = st.sidebar.selectbox('What part of the world do you want to select?',
    #                              country['Part_of_World'].unique())
    
    option_world = st.sidebar.selectbox('What part of the world do you want to select?',
                                  pd.read_sql_query(query_part_of_world,db.conn))

    query_country = ("SELECT DISTINCT name "
                     "FROM public.country "
                     "WHERE partofworld='{0}'; ").format(option_world)
    
    option_country = st.sidebar.selectbox('What country would you like to visualize?',
                                    pd.read_sql_query(query_country,db.conn))
                                  #country[country['Part_of_World']==option_world]['Country Name'].unique())


    st.markdown("### Pollution visualization")

    query1 = ("SELECT year,co2"
              "FROM public.pollution P"
              "WHERE P.cname={0}"
              "ORDER BY year").format(option_country)


    result = pd.read_sql_query(query1,db.conn)
    st.write("How much CO2 has this country emitted over the years?")
    fig = px.bar(result, x="year", y="co2", text='co2')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig)