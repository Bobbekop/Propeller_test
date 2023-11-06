import streamlit as st
import math

def parameter_controls():

    tab1, tab2, tab3 = st.tabs(["Propeller","Hub","Blade"])
    
    #PROPELLER PARAMETERS
    with tab1:
        num_of_blades=st.number_input("Number of Blades",min_value=1, value = 2, max_value= 12)
        propeller_diameter_inch=st.number_input("Propeller Diameter(Inch)",min_value=3, value=6,max_value=15)
        pitch_inch=st.number_input("Pitch(Inch)",min_value=0,value=4,max_value=10)
        chord_scale=st.number_input("Chord Scale",min_value=0.01,value=0.15,max_value=0.25,step=0.01,format="%.2f")
        tip_size=st.number_input("Tip Size",min_value=0.01,value=5.0,max_value=15.0,step=0.1,format="%.1f")
        
    #HUB and COUNTERWEIGHT PARAMETERS
    with tab2:
       col1,col2,col3 = st.columns(3)
       with col1:
           hub_diam = st.number_input("Hub Diameter",min_value=3.0,value = 13.0,max_value=50.0,step=0.1,format="%.1f")
           hub_height = st.number_input("Hub Height",min_value=3.0,value = 7.0, max_value=50.0,step=0.1,format="%.1f")
           hub_hole_diam=st.number_input("Hub Hole Diameter",min_value=1.0,value=5.0,max_value=49.0,step=0.1,format="%.1f")
       with col2:
           hub_hole_chamf_diam=st.number_input("Hub Chamfer Diameter",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_up_chamf_depth=st.number_input("Hub Chamfer Upper Depth",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_low_chamf_depth=st.number_input("Hub Chamfer Lower Depth",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
       with col3:
           bolt_mm=st.number_input("Bolt Size mm",min_value=3,value=5,max_value=8)
           bolt_top_mm=st.number_input("Bolt Top thickness mm",min_value=2.0,value=3.5,max_value=8.0,step=0.1,format="%.1f")
           bolt_top_width_mm=st.number_input("Bolt Top Width mm",min_value=3.0,value=7.9,max_value=10.0,step=0.1,format="%.1f")
    #BLADE PARAMETERS
    with tab3:
        root_length=st.number_input("Root Length",min_value=0.5,value=10.0,max_value=30.0,step=0.1,format="%.1f")
        num_of_sections=st.number_input("Number of Sections",min_value=1,value=10,max_value=50)
        blade_thickness=st.number_input("Blade Thickness",min_value=0.1,value=1.0,max_value=5.0,step=0.1,format="%.1f")
        
    propeller_diameter = propeller_diameter_inch*25.4
    angle_of_attack = math.degrees(math.atan(pitch_inch / (math.pi * propeller_diameter_inch)))

    return{
        'num_of_blades':num_of_blades,
        'propeller_diameter':propeller_diameter,
        'angle_of_attack':angle_of_attack,
        'chord_scale':chord_scale,
        'tip_size':tip_size,
        'hub_diam':hub_diam,
        'hub_height':hub_height,
        'hub_hole_diam':hub_hole_diam,
        'hub_hole_chamf_diam':hub_hole_chamf_diam,
        'hub_hole_up_chamf_depth':hub_hole_up_chamf_depth,
        'hub_hole_low_chamf_depth':hub_hole_low_chamf_depth,
        'root_length':root_length,
        'num_of_sections':num_of_sections,
        'blade_thickness':blade_thickness,
        'bolt_mm':bolt_mm,
        'bolt_top_mm':bolt_top_mm,
        'bolt_top_width_mm':bolt_top_width_mm}
