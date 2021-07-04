# Education section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#  from plotly.subplots import make_subplots
from apps.database_connection import DB
import apps.helper_functions as hf

# database class (to handle connecion to DB + execute and retrieve query
# results)
db = DB('dbs_project')


def app():
    gdp = pd.read_sql_query("SELECT * FROM gdp", db.conn)

    st.title('Education')

    option_country, option_world = hf.render_sidebar(db)

    # -------------------------------------------------------------------------

    st.write("Where does this country position itself \
              in a worldwide GDP ranking over the years?")
    if len(hf.get_gdp_ranking(gdp, option_country)) < 1:
        hf.no_data()
    else:
        st.dataframe(hf.get_gdp_ranking(gdp, option_country))

    st.write("What share of its GDP does this country spend on education?")

    query1 = (
        f"""
        SELECT year, share_gdp_primary, share_gdp_secondary, share_gdp_tertiary
        FROM education
        WHERE
            cname='{option_country}' AND
            (share_gdp_primary IS NOT NULL OR
             share_gdp_secondary IS NOT NULL OR
             share_gdp_tertiary IS NOT NULL)
        ORDER BY year;
        """
    )

    result1 = pd.read_sql_query(query1, db.conn)
    result1.replace(to_replace=[None], value=np.nan, inplace=True)
    if len(result1) < 1:
        hf.no_data()
    else:
        table1 = result1.rename(
            columns={'year': "Year",
                     'share_gdp_primary': "%GDP primary edu",
                     'share_gdp_secondary': "%GDP secondary edu",
                     'share_gdp_tertiary': "%GDP tertiary edu"
                    },
            inplace=False)
        st.dataframe(table1)
        fig1 = px.bar(result1, x="year", y=["share_gdp_primary",
                      "share_gdp_secondary", "share_gdp_tertiary"])
        fig1.update_layout(
            xaxis_title="Year",
            yaxis1_title="Share GDP spent on Education (%)"
        )
        st.plotly_chart(fig1)

    st.write("What is the impact of spending on primary and secondary education \
              on school completion rates?")

    query2 = (
        f"""
        SELECT year, primary_rate, secondary_rate
        FROM education
        WHERE
            cname='{option_country}' AND
            (primary_rate IS NOT NULL OR
             secondary_rate IS NOT NULL)
        ORDER BY year;
        """
    )

    result2 = pd.read_sql_query(query2, db.conn)
    if len(result2) < 1:
        hf.no_data()
    else:
        table2 = result2.rename(
            columns={'year': "Year",
                     'primary_rate': "Rate primary edu",
                     'secondary_rate': "Rate secondary edu",
                    },
            inplace=False)
        st.dataframe(table2)
        fig2 = px.bar(result2,
                      x="year",
                      y=["primary_rate", "secondary_rate"], barmode='group')
        fig2.layout.xaxis.title = "Year"
        fig2.layout.yaxis.title = "Completion rate"
        hf.custom_legend_name(fig2, ['Primary school', 'Secondary school'])

        st.plotly_chart(fig2)

    if st.sidebar.button('Disconnect from database?'):
        db.close_connection()
        st.markdown('Disconnected from database! Bye bye! :wave:')
