# Security section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
#  from plotly.subplots import make_subplots
from apps.database_connection import DB

# directory management
wdir = os.getcwd()
ddir = os.path.join(wdir, 'data')
raw_ddir = os.path.join(ddir, 'raw')
final_ddir = os.path.join(ddir, 'final')

# database class (to handle connecion to DB + execute and retrieve query
# results)
db = DB('dbs_project')


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


def app():
    gdp = pd.read_sql_query("SELECT * FROM gdp", db.conn)

    st.title('Security')

    query_part_of_world = (
            """
            SELECT DISTINCT partofworld
            FROM country;
            """
    )

    option_world = st.sidebar.selectbox(
        "What part of the world do you want to select?",
        pd.read_sql_query(query_part_of_world, db.conn)
    )

    query_country = (
            f"""
            SELECT DISTINCT name
            FROM country
            WHERE partofworld='{option_world}';
            """
    )

    option_country = st.sidebar.selectbox(
            "What country would you like to visualize?",
            pd.read_sql_query(query_country, db.conn)
    )

    # -------------------------------------------------------------------------

    if not len(get_gdp_ranking(gdp, option_country)):
        st.markdown("There is no data available for this \
                    country :disappointed:")
    else:
        st.dataframe(get_gdp_ranking(gdp, option_country))

    st.write("Is there a relationship between unemployment \
              rate and homicide rate?")

    query1 = (
        f"""
        SELECT year, unemployment_rate, homicide_rate
        FROM security
        WHERE cname='{option_country}'
        ORDER BY year;
        """
    )

    result = pd.read_sql_query(query1, db.conn)
    if not len(result):
        st.markdown("There is no data available for this \
                    country :disappointed:")
    else:
        st.dataframe(result)
        fig = px.scatter(result, x="year", y="unemployment_rate",
                         size='homicide_rate')
        st.plotly_chart(fig)

    
    st.write("What is the human rights situation of this country?")

    query2 = ("SELECT S.year,S.hr_score,S.hr_violations "
              "FROM public.security S "
              "WHERE S.cname='{0}' "
              "ORDER BY S.year; ").format(option_country)

    result2 = pd.read_sql_query(query2,db.conn)
    if len(result2)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        st.dataframe(result2)
        fig2 = px.scatter(result2, x="year", y="hr_score")
        st.plotly_chart(fig2)

    st.write("For some countries there is data on happiness scores: will happier people work less on average?")

    query3 = ("SELECT S.year,S.happiness,S.avg_annual_working_hours "
              "FROM public.security S "
              "WHERE S.cname='{0}' "
              "ORDER BY S.year; ").format(option_country)

    result3 = pd.read_sql_query(query3,db.conn)
    if len(result3)==0:
        st.markdown("There is no data available for this country :disappointed:")
    else:
        st.dataframe(result3)
        #fig3 = px.scatter(result3, x="year", y="happiness")
        fig3 = go.Figure()

        fig3.add_trace(
            go.Scatter(
                x=result3.year,
                y=result3.avg_annual_working_hours,
                mode='lines+markers',
                name='Average annual working hours'
            ))

        fig3.add_trace(
            go.Bar(
                x=[0, 1, 2, 3, 4, 5],
                y=[1, 0.5, 0.7, -1.2, 0.3, 0.4]
            ))
        st.plotly_chart(fig3)


    if st.sidebar.button('Disconnect from database?'):
        db.close_connection()
        st.markdown('Disconnected from database! Bye bye! :wave:')

