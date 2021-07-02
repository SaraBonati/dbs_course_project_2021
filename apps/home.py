# Home section of the DBS Project dashboard
# (the multi-app framework is taken from https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import numpy as np

home_text = """

            <style>
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300&display=swap');
            body {
                font-family: 'IBM Plex Mono', sans-serif;
                color: rgba(0, 0, 0, 0.8);
                font-size: 20px;
                padding: 70px;
                }
            </style>

            <body> 

            <h1 align=center> Home </h1>
            <h2 align=center> Group </h2>
            <p align=center> Sara Bonati (Student ID: 5314260) \ Elica Tokmakchieva (Student ID: 5233090) \ Tobias Sandmann (Student ID: 5479422) </p>

            <h2 align=center> What is our project about? </h2>
            <p align=center> Gross Domestic Product (GDP) is one of the main indicators used to represent economical status,
            measuring the value of the final goods and services produced in a country. 
            While this indicator provides a summary measure of economic health, it also
            provides few insights over aspects such as happiness or education. An online article by [Eurostat](https://ec.europa.eu/eurostat) 
            provides an overview of 9+1 Quality of Life indicators, aspects proposed in the article to  </p>
            <h2 align=center> What is our application? </h2>
            <p align=center> We create an interactive dashboard where users can select a country of interest and visualize the relationship
            between GDP and selected quality fo life indicators. Note that some countries have missing data for some
            indicators: this will be signaled by the application.\
            As countries see their GDP increase over the years does the quality of life follow this increase over
            all its possible facets? As the economy grows and more funds are put into e.g. education and health,
            do the quality of these services also increase?  \ </p>

            <h2 align=center> How do I get started? </h2>
            <p align=center> First, select one of the pages of the application form the bullet point menu on the top
            part of the selector on the left side of the screen. In each applicaiton the left side of 
            the screen will contain a slider that allows the user to choose first "part of the world", 
            the the country of interest, and finally a time period to visualize the data from the database
            (subject to constraints depending on the available years for the data). </p>
            </body>
            """
def app():
    st.markdown(home_text, unsafe_allow_html=True)