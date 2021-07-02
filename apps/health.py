# Health section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import os
import plotly.express as px
from plotly.subplots import make_subplots
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

    st.title('Health')

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

    st.write("Where does this country position itself \
             in the world with respect to GDP?")
    if not len(get_gdp_ranking(gdp, option_country)):
        st.markdown("There is no data available for this \
                    country :disappointed:")
    else:
        st.dataframe(get_gdp_ranking(gdp, option_country))

    st.write("What share of its GDP does this country spend on health?")

    query1 = (
        f"""
        SELECT G.year, G.value, H.share_gdp_health
        FROM gdp G, health H
        WHERE
            G.cname=H.cname
            AND G.year=H.year
            AND G.cname='{option_country}';
        """
    )

    result = pd.read_sql_query(query1, db.conn)
    if not len(result):
        st.markdown("There is no data available for this \
                    country :disappointed:")
    else:
        st.dataframe(result)
        fig1 = px.bar(result, x="year", y="share_gdp_health")
        st.plotly_chart(fig1)

    st.write("What about mental health in this country?")

    query2 = (
        f"""
        SELECT G.year, G.value, H.mental_health_daly, H.mental_health_share
        FROM gdp G, health H
        WHERE
            G.cname=H.cname
            AND G.year=H.year
            AND G.cname='{option_country}';
        """
    )

    result2 = pd.read_sql_query(query2, db.conn)
    if not len(result2):
        st.markdown("There is no data available for this \
                    country :disappointed:")
    else:
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        # Create two independent figures with px.line each containing data from
        # multiple columns
        fig1 = px.line(result2, x='year', y='mental_health_daly')
        fig2 = px.line(result2, x='year', y='mental_health_share')
        fig2.update_traces(yaxis="y2")

        subfig.add_traces(fig1.data + fig2.data)
        subfig.layout.xaxis.title = "Year"
        subfig.layout.yaxis.title = "Mental health impact (DALY units)"
        subfig.layout.yaxis2.title = "Share of population with mental \
                                      health problems"
        # Recoloring is necessary otherwise lines from fig1 und fig2 would
        # share each color e.g. Linear-, Log- = blue; Linear+, Log+ = red
        # ... we don't want this
        subfig.for_each_trace(
            lambda t: t.update(line=dict(color=t.marker.color)))
        st.plotly_chart(subfig)

    if st.sidebar.button("Disconnect from database?"):
        db.close_connection()
        st.markdown("Disconnected from database! Bye bye! :wave:")

