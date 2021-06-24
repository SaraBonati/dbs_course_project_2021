# Education section of the DBS Project dashboard
# (the multi-app framework is taken from https://github.com/upraneelnihar/streamlit-multiapps)

import streamlit as st
import pandas as pd
import numpy as np


def app():
    st.title('Education')

    st.write("This is a sample health page in the mutliapp.")
    st.write("See `apps/education.py` to know how to use it.")

    st.markdown("### Education visualization")
