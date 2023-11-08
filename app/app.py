import streamlit as st
from uuid import uuid4
import glob
import time
from datetime import datetime, date
from pathlib import Path
from controls import (
    sidebar, 
    parameter_controls, 
    parameter_controls_layers,
    model_controls,
    file_controls,
    code_view
)

def make_tabs():
    tab_parameters, tab_file_controls,tab_layer= st.tabs(["Parameters", "File","Layers",])
    
    with tab_parameters:
        model_parameters = parameter_controls()
    with tab_file_controls:
        ui_file_controls = file_controls()
    with tab_layer:
        add_button, dupe = parameter_controls_layers()    
    
    parameters = model_parameters | dupe
    
    return add_button, parameters, ui_file_controls

def initialize_session():
    if 'models' not in st.session_state:
        st.session_state['models'] = []

    if "session_id" not in st.session_state:
        st.session_state['session_id'] = uuid4()

def ui_model_controls(model_parameters, ui_file_controls):
    col1, col2, col3 = st.columns(3)
    with col1:
        generate_button = st.button('Generate Model')
    with col2:
        color = st.color_picker('Model Color', '#E06600', label_visibility="collapsed")
    with col3:
        render = st.selectbox("Render", ["material", "wireframe"], label_visibility="collapsed")

    model_controls(model_parameters,color,render,ui_file_controls)

def handle_add_button_click(add_model_layer_button, model_parameters):
    if add_model_layer_button:
        # fix layer name dupes
        if len(st.session_state['models']) > 0:
            for model in st.session_state['models']:
                if model_parameters['layer_name']==model['layer_name']:
                    model_parameters['layer_name'] += " copy"

        st.session_state['models'].append(model_parameters)
        st.experimental_rerun()

def start_app():
    add_model_layer_button, model_parameters, ui_file_controls = make_tabs()
    st.divider()
    ui_model_controls(model_parameters, ui_file_controls)
    handle_add_button_click(add_model_layer_button, model_parameters)

def clean_up_static_files():
    files = glob.glob("app/static/model_*.stl")
    today = datetime.today()
    for file_name in files:
        file_path = Path(file_name)
        modified = file_path.stat().st_mtime
        modified_date = datetime.fromtimestamp(modified)
        delta = today - modified_date
        if delta.total_seconds() > 1200:
            file_path.unlink()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Propeller Test",
        page_icon="🛬"
    )
    initialize_session()
    start_app()
    sidebar()
    clean_up_static_files()
