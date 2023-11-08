import streamlit as st
from uuid import uuid4
import glob
import time
from datetime import datetime, date
from pathlib import Path
from controls import (
    sidebar, 
    parameter_controls, 
    model_controls,
    file_controls,
    camera_controls
)

def ui():

    camera_control=camera_controls()
    
    tab1, tab2 = st.tabs(["Parameters", "File"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        model_parameters = parameter_controls()
    with tab2:
        file_control = file_controls()

    col1, col2, col3= st.columns(3)
    with col1:
        render = st.checkbox('Render:', False)
    with col2:
        color1 = st.color_picker('Primary Color', '#00f900', disabled=not render)
    with col3:
        color2 = st.color_picker('Secondary Color', '#0011f9', disabled=not render)

    if render:
        model_controls(
            model_parameters, 
            camera_control, 
            color1, 
            color2, 
            file_control
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Propeller Test",
        page_icon="🛬"
    )

    st.title('Propeller Test')
    ui()
    sidebar()
