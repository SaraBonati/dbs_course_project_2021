# This script defines the streamlit components for the interactive dashboard 
# application built for the Database Systems Project Assignment.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
#---------------------------------------------------------------------------

# general utility import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time
import os
import psycopg2
from config import config

# directory management
wdir = os.getcwd()                    # working directory
sdir = os.path.join(wdir,'scripts')   # scripts directory
ddir = os.path.join(wdir,'data')      # data directory

# APP
#--------------------------------------------------------------------------
# intro to app
st.title('DBS Project')
st.write('Test 1234')

option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])


# progress bar
# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)