import streamlit as st
import streamlit.components.v1 as components
import cadquery as cq
import os
import time
from .modelGeneration import (
    generate_propeller
)

EXPORT_NAME = 'Propeller_model'
PREVIEW_NAME = 'Propeller_preview.svg'

def generate_model(parameters):
    model = generate_propeller(parameters)
    scene = cq.Workplane("XY").union(model)
    
    return scene

def generate_stl_preview(color, render):
    with open("js/three.min.js", "r") as js_file:
        three_js = js_file.read()

    with open("js/STLLoader.js", "r") as js_file:
        stl_loader = js_file.read()

    with open("js/OrbitControls.js", "r") as js_file:
        orbital_controls = js_file.read()

    with open("js/stl-viewer.js", "r") as js_file:
        stl_viewer_component = (
            js_file.read()
            .replace('{__REPLACE_COLOR__}',f'0x{color[1:]}')
            .replace('{__REPLACE_MATERIAL__}',render)
        )
        
    session_id = st.session_state['session_id']
    components.html(
        r'<div style="height:500px">'+
        r'<script>'+
        three_js+' '+
        stl_loader+' '+
        orbital_controls+' '+
        'console.log(\'frizzle\');'+
        stl_viewer_component+' '+
        r'</script>'+
        r'<stl-viewer model="./app/static/model_'+str(session_id)+'.stl?cache='+str(time.time())+r'"></stl-viewer>'+
        r'</div>',
        height = 500
    )

def model_controls(parameters,color,render,file_controls):
    start = time.time()
    
    with st.spinner('Generating Model..'):
        download_name = file_controls['Name']
        export_type = file_controls['Type'] 
        model = generate_model(parameters)

        cq.exporters.export(model,f'{EXPORT_NAME}.{export_type}')
        cq.exporters.export(model,'app/static/'+f'{EXPORT_NAME}_{session_id}.stl')
        
        end = time.time()

        generate_stl_preview(color, render)

        if f'{EXPORT_NAME}.{export_type}' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            with open(f'{EXPORT_NAME}.{export_type}', "rb") as file:
                btn = st.download_button(
                        label=f"Download {export_type}",
                        data=file,
                        file_name=f'{download_name}.{export_type}',
                        mime=f"model/{export_type}"
                    )
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")
    
