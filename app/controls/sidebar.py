import streamlit as st

def sidebar():
    with st.sidebar:
        st.title('Propeller Generator Test')
        st.write('This is a test app, testing the functionality of a parametric propeller design for UAVs, using CadQuery.')
        st.markdown("[Get an Airfoil](http://airfoiltools.com/search/index)")
