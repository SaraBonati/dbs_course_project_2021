# This script defines the streamlit components for the interactive dashboard 
# application built for the Database Systems SS2021 Project Assignment.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
#---------------------------------------------------------------------------

# modules import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time
import os
import psycopg2
from multiapp import MultiApp
from apps import home, health, pollution, education, security # import your app modules here


# directory management
wdir = os.getcwd()                    # working directory
sdir = os.path.join(wdir,'scripts')   # scripts directory
ddir = os.path.join(wdir,'data')      # data directory


app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Health", health.app)
app.add_app("Pollution", pollution.app)
app.add_app("Education", education.app)
app.add_app("Security", security.app)

# The main app
app.run()


