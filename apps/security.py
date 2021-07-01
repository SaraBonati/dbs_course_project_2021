# Security section of the DBS Project dashboard
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
    st.title('Education')
    
    # import data (note: I am using the csv file only for the ranking)
    health = pd.read_csv(os.path.join(final_data_dir,'HEALTH.csv'),header=0)
    country = pd.read_csv(os.path.join(final_data_dir,'COUNTRY.csv'),header=0)
    gdp = pd.read_csv(os.path.join(final_data_dir,'GDP.csv'),header=0)

    query_part_of_world = """
                          SELECT DISTINCT partofworld
                          FROM public.country;  
                          """
    
    option_world = st.sidebar.selectbox('What part of the world do you want to select?',
                                  pd.read_sql_query(query_part_of_world,db.conn))

    query_country = ("SELECT DISTINCT name "
                     "FROM public.country "
                     "WHERE partofworld='{0}'; ").format(option_world)
    
    option_country = st.sidebar.selectbox('What country would you like to visualize?',
                                    pd.read_sql_query(query_country,db.conn))

    #------------------------------------------------------------------------------------

    st.write("Where does this country position itself in the world with respect to GDP?")
    if len(get_gdp_ranking(gdp,option_country))==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        st.dataframe(get_gdp_ranking(gdp,option_country))

    st.write("Is there a relationship between unemployment rate and homicide rate?")

    query1 = ("SELECT S.year,S.unemployment_rate,S.homicide_rate "
              "FROM public.security S "
              "WHERE S.cname='{0}' "
              "ORDER BY S.year; ").format(option_country)

    result = pd.read_sql_query(query1,db.conn)
    if len(result)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        st.dataframe(result)
        fig = px.scatter(result, x="year", y="unemployment_rate",size='homicide_rate')
        st.plotly_chart(fig)

    if st.sidebar.button('Disconnect from database?'):
        db.close_connection()
        st.markdown('Disconnected from database! Bye bye! :wave:')