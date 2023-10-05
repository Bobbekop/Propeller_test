import streamlit as st

def parameter_controls():

    tab1, tab2, tab3 = st.tabs(["Propeller","Hub","Blade"])
    
    #PROPELLER PARAMETERS
    with tab1:
        num_of_blades=st.number_input("Number of Blades",min_value=1, value = 2, max_value= 12)
        propeller_diameter=st.number_input("Propeller Diameter",min_value=30.0, value=180.0,max_value=300.0,step=0.5,format="%.1f")
        angle_of_attack=st.number_input("Angle of Attack",min_value=0.00,value=3.00,max_value=45.00,step=0.25,format="%.2f")
        chord_scale=st.number_input("Chord Scale",min_value=0.01,value=0.1,max_value=0.25,step=0.01,format="%.2f")
        tip_size=st.number_input("Tip Size",min_value=0.01,value=0.1,max_value=5.0,step=0.1,format="%.1f")
        
    #HUB PARAMETERS
    with tab2:
       col1,col2 = st.columns(2)
       with col1:
           hub_diam = st.number_input("Hub Diameter",min_value=3.0,value = 14.0,max_value=50.0,step=0.1,format="%.1f")
           hub_height = st.number_input("Hub Height",min_value=3.0,value = 7.0, max_value=50.0,step=0.1,format="%.1f")
           hub_hole_diam=st.number_input("Hub Hole Diameter",min_value=1.0,value=6.2,max_value=49.0,step=0.1,format="%.1f")
       with col2:
           hub_hole_chamf_diam=st.number_input("Hub Chamfer Diameter",min_value=1.0,value=10.0,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_up_chamf_depth=st.number_input("Hub Chamfer Upper Depth",min_value=1.0,value=1.0,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_low_chamf_depth=st.number_input("Hub Chamfer Lower Depth",min_value=1.0,value=3.25,max_value=50.0,step=0.25,format="%.2f")
     
    #BLADE PARAMETERS
    with tab3:
        root_length=st.number_input("Root Length",min_value=0.5,value=5.0,max_value=20.0,step=0.1,format="%.1f")
        num_of_sections=st.number_input("Number of Sections",min_value=1,value=10,max_value=50)
  
    return{
        #PROPELLER PARAMETERS
        'num_of_blades':num_of_blades,
        'propeller_diameter':propeller_diameter,
        'angle_of_attack':angle_of_attack,
        'chord_scale':chord_scale,
        'tip_size':tip_size,
        #HUB PARAMETERS
        'hub_diam':hub_diam,
        'hub_height':hub_height,
        'hub_hole_diam':hub_hole_diam,
        'hub_hole_chamf_diam':hub_hole_chamf_diam,
        'hub_hole_up_chamf_depth':hub_hole_up_chamf_depth,
        'hub_hole_low_chamf_depth':hub_hole_low_chamf_depth,
        #BLADE PARAMETERS
        'root_length':root_length,
        'num_of_sections':num_of_sections}