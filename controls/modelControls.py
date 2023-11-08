import streamlit as st
import cadquery as cq
import os
import time
from .modelGeneration import (
    generate_propeller
)

EXPORT_NAME = 'Propeller_model'
PREVIEW_NAME = 'Propeller_preview.svg'

def generate_model(parameters):
    propeller = generate_propeller(parameters)
    
    return propeller

def generate_preview(model, image_name, color1, color2, camera):
    hex_1 = color1.lstrip('#')
    rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

    hex_2 = color2.lstrip('#')
    rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
    
    cq.exporters.export(model, image_name, opt={
        "projectionDir": (camera['axis1'], camera['axis2'], camera['axis3']),
        "showAxes": True,
        "focus": camera['focus'],
        "strokeColor": rgb_1,
        "hiddenColor": rgb_2})
    
def model_controls(parameters,camera,color1,color2,file_controls):
    start = time.time()
    
    with st.spinner('Generating Model..'):
        download_name = file_controls['Name']
        export_type = file_controls['Type'] 
        model = generate_model(parameters)

        cq.exporters.export(model,f'{EXPORT_NAME}.{export_type}')
        generate_preview(model, PREVIEW_NAME, color1, color2, camera)

        end = time.time()

        st.write("Preview:")
        st.image(PREVIEW_NAME)

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
    
