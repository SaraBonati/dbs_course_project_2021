# Security section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import plotly.express as px
from apps.database_connection import DB
import apps.helper_functions as hf

# database class (to handle connecion to DB + execute and retrieve query
# results)
db = DB('dbs_project')


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
    st.write("Where does this country position itself \
              in the world with respect to GDP?")
    if not len(hf.get_gdp_ranking(gdp, option_country)):
        hf.no_data()
    else:
        st.dataframe(hf.get_gdp_ranking(gdp, option_country))

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
    if len(result) < 1:
        hf.no_data()
    else:
        st.dataframe(result)
        fig = px.scatter(result,
                         x="year",
                         y="unemployment_rate",
                         size='homicide_rate')
        st.plotly_chart(fig)

    st.write("What is the human rights situation of this country, \
              epxressed in Human Rights (HR) Score?")

    query2 = (
        f"""
        SELECT year,hr_score
        FROM security
        WHERE cname='{option_country}'
        ORDER BY year;
        """
        )

    query2_avg = (
        f"""
        SELECT year, AVG(hr_score) AS avghr
        FROM security
        WHERE cname IN (SELECT name
                        FROM country
                        WHERE partofworld='{option_world}')
        GROUP BY year
        ORDER BY year;
        """
    )

    result2 = pd.read_sql_query(query2, db.conn)
    result2_avg = pd.read_sql_query(query2_avg, db.conn)

    if len(result2) < 1:
        hf.no_data()
    else:
        st.dataframe(result2)

        fig2 = px.line(result2,
                       x='year',
                       y=[result2['hr_score'], result2_avg["avghr"]])
        fig2.layout.xaxis.title = "Year"
        fig2.layout.yaxis.title = "HR Score"
        hf.custom_legend_name(fig2, ['Country HR Score', f'Average HR score in {option_world}'])

        st.plotly_chart(fig2)

    #  st.write("For some countries there is data on happiness scores: \
              #  will happier people work less on average?")

    #  query3 = (
        #  f"""
        #  SELECT year, happiness, avg_annual_working_hours
        #  FROM security
        #  WHERE cname='{option_country}'
        #  ORDER BY year;
        #  """
    #  )

    if st.sidebar.button('Disconnect from database?'):
        db.close_connection()
        st.markdown('Disconnected from database! Bye bye! :wave:')

