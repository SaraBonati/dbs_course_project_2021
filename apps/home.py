# Home section of the DBS Project dashboard
# (the multi-app framework is taken from https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import numpy as np


def app():
    st.title('Home')

    st.write("This is a sample home page in the mutliapp.")
    st.write("See `apps/home.py` to know how to use it.")

    st.markdown("### Sample Data")

    st.write('Navigate to `Data Stats` page to visualize the data')