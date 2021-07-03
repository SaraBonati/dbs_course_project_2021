# Home section of the DBS Project dashboard
# (the multi-app framework is taken from
# https://github.com/upraneelnihar/streamlit-multiapps)

import os
from pathlib import Path
import streamlit as st


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def app():
    script_dir = os.path.dirname(__file__)
    home_markdown = read_markdown_file(os.path.join(script_dir, "home.md"))
    st.markdown(home_markdown, unsafe_allow_html=True)
