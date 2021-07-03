# Pollution section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from apps.database_connection import DB
import apps.helper_function as hf


# database class (to handle connecion to DB + execute and retrieve query
# results)
db = DB('dbs_project')


def app():
    #  gdp = pd.read_sql_query("SELECT * FROM gdp", db.conn)

    st.title('Pollution')

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

    # ------------------------------------------------------------------------

    query1 = (
        f"""
        SELECT year, co2
        FROM pollution
        WHERE cname='{option_country}'
        ORDER BY year;
        """
    )

    query2 = (
        f"""
        SELECT year, SUM(co2) AS sumco2
        FROM pollution
        WHERE cname IN (SELECT name
                        FROM country
                        WHERE partofworld='{option_world}')
        GROUP BY year
        ORDER BY year;
        """
    )

    query3 = (
        f"""
        SELECT year, indoor_death_rate, outdoor_death_rate
        FROM pollution P
        WHERE
            cname='{option_country}' AND
            year >= 1990
        ORDER BY year;
        """
    )

    st.write("How much CO2 has this country emitted over the years?")

    result1 = pd.read_sql_query(query1, db.conn)
    if len(result1) < 1:
        hf.no_data()
    else:
        fig1 = px.line(result1, x="year", y="co2")
        fig1.update_traces(texttemplate='%{text:.2s}',
                           textposition='bottom right')
        fig1.update_layout(
            xaxis_title="Year",
            yaxis_title=r"CO₂ [t]"
        )
        st.plotly_chart(fig1)

    result2 = pd.read_sql_query(query2, db.conn)
    st.write("How much CO2 overall has the part of the \
              world of this country emitted over the years?")
    if len(result2) < 1:
        hf.no_data()
    else:
        fig2 = px.bar(result2, x="year", y="sumco2")
        fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig2.update_layout(
            xaxis_title="Year",
            yaxis_title=r"Σ CO₂ [t]"
        )
        st.plotly_chart(fig2)

    result3 = pd.read_sql_query(query3, db.conn)
    st.write("What are the indoor and outdoor death rates \
              realted to pollution in this country?")
    if len(result3) < 1:
        hf.no_data()
    else:
        st.dataframe(result3)
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        # create two independent figures with px.line each containing data from
        # multiple columns
        fig1 = px.line(result3, x='year', y='indoor_death_rate')
        fig2 = px.line(result3, x='year', y='outdoor_death_rate')
        fig2.update_traces(yaxis="y2")

        subfig.add_traces(fig1.data + fig2.data)
        subfig.layout.xaxis.title = "Year"
        subfig.layout.yaxis.title = "Indoor death rate"
        subfig.layout.yaxis2.title = "Outdoor death rate"
        # Recoloring is necessary otherwise lines from fig1 und fig2 would
        # share each color e.g. Linear-, Log- = blue; Linear+, Log+ = red
        # ... we don't want this
        subfig.for_each_trace(
            lambda t: t.update(line=dict(color=t.marker.color)))
        st.plotly_chart(subfig)

    if st.sidebar.button("Disconnect from database?"):
        db.close_connection()
        st.markdown("Disconnected from database! Bye bye! :wave:")
