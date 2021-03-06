# Health section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from apps.database_connection import DB
import apps.helper_functions as hf

# database class (to handle connecion to DB + execute and retrieve query
# results)
db = DB('dbs_project')


def app():
    gdp = pd.read_sql_query("SELECT * FROM gdp", db.conn)

    st.title('Health')

    option_country, option_world = hf.render_sidebar(db)

    # -------------------------------------------------------------------------

    st.write("Where does this country position itself \
              in a worldwide GDP ranking over the years?")
    if len(hf.get_gdp_ranking(gdp, option_country)) < 1:
        hf.no_data()
    else:
        st.dataframe(hf.get_gdp_ranking(gdp, option_country))

    st.write("What share of its GDP does this country spend on health?")

    query1 = (
        f"""
        SELECT G.year, G.value, H.share_gdp_health
        FROM gdp G, health H
        WHERE
            G.cname=H.cname AND
            G.year=H.year AND
            G.year>=1994 AND
            G.cname='{option_country}';
        """
    )

    result1 = pd.read_sql_query(query1, db.conn)
    result1.replace(to_replace=[None], value=np.NaN, inplace=True)
    result1['health_value'] = result1['share_gdp_health'] \
        .apply(lambda x: (x / 100) if pd.notnull(x) else x) * result1['value']
    if len(result1) < 1:
        hf.no_data()
    else:
        table1 = result1.rename(
            columns={'year': "Year",
                     'value': "GDP [US$]",
                     'share_gdp_health': "GDP on Health [%]",
                     'health_value': "GDP on Health [US$]"},
            inplace=False)
        st.dataframe(table1)
        fig1 = px.bar(result1, x="year", y=["value", "health_value"])
        fig1.layout.xaxis.title = "Year"
        fig1.layout.yaxis.title = "US$"
        hf.custom_legend_name(fig1, ['Total GDP', 'Health GDP'])

        st.plotly_chart(fig1, use_container_width=True)

    st.write("What about mental health in this country?")

    query2 = (
        f"""
        SELECT G.year, G.value, H.mental_health_daly, H.mental_health_share
        FROM gdp G, health H
        WHERE
            G.cname=H.cname AND
            G.year=H.year AND
            G.year>=1990 AND
            G.cname='{option_country}';
        """
    )

    result2 = pd.read_sql_query(query2, db.conn)
    if len(result2) < 1:
        hf.no_data()
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
        subfig.layout.yaxis2.title = "Share of population with mental health problems"
        # Recoloring is necessary otherwise lines from fig1 und fig2 would
        # share each color e.g. Linear-, Log- = blue; Linear+, Log+ = red
        # ... we don't want this
        subfig.for_each_trace(
            lambda t: t.update(line=dict(color=t.marker.color)))
        st.plotly_chart(subfig, use_container_width=True)

    if st.sidebar.button("Disconnect from database?"):
        db.close_connection()
        st.markdown("Disconnected from database! Bye bye! :wave:")
