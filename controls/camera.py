import streamlit as st

def camera_controls():
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        axis1 = st.number_input("axis1",step=45,value=0)
    with col2:
        axis2 = st.number_input("axis2",step=45,value=0)
    with col3:
        axis3 = st.number_input("axis3",step=45, value=-1)

    focus = st.number_input("Focus",step=1, value=50)
    """
    return {
        'axis1':axis1 = 0, 
        'axis2':axis2 = 0, 
        'axis3':axis3 = -1, 
        'focus':focus = 50
    }
