# This script defines the streamlit components for the interactive dashboard
# application built for the Database Systems SS2021 Project Assignment.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
# --------------------------------------------------------------------------

# modules import
import os
from multiapp import MultiApp
# Import all apps here
from apps import home, health, pollution, education, security


# directory management
wdir = os.getcwd()                     # working directory
ddir = os.path.join(wdir, 'data')      # data directory


app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Health", health.app)
app.add_app("Pollution", pollution.app)
app.add_app("Education", education.app)
app.add_app("Security", security.app)

# The main app
app.run()
