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
        r = df[df['Year']==year].sort_values(by='co2emissions', ascending=False).reset_index()
        idx = r.index[r['Country Name']==option_country][0]
        rankings.append(idx+1)
    return  pd.DataFrame({'Year': years,
                          'Ranking':rankings})


def app():
    # import data (note: I am using the csv file for the rankings only)
    health = pd.read_csv(os.path.join(final_data_dir,'HEALTH.csv'),header=0)
    country = pd.read_csv(os.path.join(final_data_dir,'COUNTRY.csv'),header=0)
    pollution = pd.read_csv(os.path.join(final_data_dir,'POLLUTION.csv'),header=0)

    st.title('Pollution')

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

    #---------------------------------------------------------------

    query1 = ("SELECT P.year,P.co2 "
              "FROM public.pollution P "
              "WHERE P.cname='{0}' "
              "ORDER BY P.year; ").format(option_country)


    query2 = ("SELECT P.year,SUM(P.co2) AS sumco2 "
             "FROM public.pollution P "
             "WHERE P.cname IN (SELECT C.name "
             "                   FROM public.country C "
             "                   WHERE C.partofworld='{0}') "
             "GROUP BY P.year "
             "ORDER BY P.year; ").format(option_world)

    query3 = ("SELECT P.year,P.indoor_death_rate,P.outdoor_death_rate "
             "FROM public.pollution P "
             "WHERE P.cname='{0}' "
             "AND P.year>= 1990 "
             "ORDER BY P.year; ").format(option_country)


    result = pd.read_sql_query(query1,db.conn)
    st.write("How much CO2 has this country emitted over the years?")
    if len(result)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        fig = px.bar(result, x="year", y="co2", text='co2')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig)

    result2 = pd.read_sql_query(query2,db.conn)
    st.write("How much CO2 overall has the part of the world of this country emitted over the years?")
    if len(result2)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        fig2 = px.bar(result2, x="year", y="sumco2")
        fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig2)

    result3 = pd.read_sql_query(query3,db.conn)
    st.write("What are the indoor and outdoor death rates realted to pollution in this country?")
    if len(result3)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        st.dataframe(result3)
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        # create two independent figures with px.line each containing data from multiple columns
        fig = px.line(result3, x='year',y='indoor_death_rate')
        fig2 = px.line(result3,x='year',y='outdoor_death_rate')
        fig2.update_traces(yaxis="y2")

        subfig.add_traces(fig.data + fig2.data)
        subfig.layout.xaxis.title="Year"
        subfig.layout.yaxis.title="Indoor death rate"
        subfig.layout.yaxis2.title="Outdoor death rate"
        # recoloring is necessary otherwise lines from fig und fig2 would share each color
        # e.g. Linear-, Log- = blue; Linear+, Log+ = red... we don't want this
        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        st.plotly_chart(subfig)

    if st.sidebar.button('Disconnect form database?'):
        db.close_connection()
        st.markdown('Bye bye! :wave:')