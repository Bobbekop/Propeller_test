import streamlit as st

def file_controls():
    
    col1, col2 = st.columns(2)
    
    with col1:
        download_name = st.text_input('File Name','Model')
    with col2:
        export_type = st.selectbox("File type",('stl','step'))
    return {
        'Name':download_name,
        'Type':export_type
    }
