import streamlit as st
import math

def parameter_controls():

    propeller_parameters, hub_and_counterweight_parameters, blade_parameters = st.tabs(["Propeller","Hub","Blade"])


    with propeller_parameters:
        num_of_blades=st.number_input("Number of Blades",min_value=1, value = 2, max_value= 12)
        propeller_diameter_inch=st.number_input("Propeller Diameter(Inch)",min_value=2.0, value=6.0,max_value=15.0,step=0.1,format="%.1f")
        #propeller_diameter_mm=st.number_input("Propeller Diameter(mm)",min_value=50.0, value=152.4,max_value=381,step=0.1,format="%.1f")
        pitch_inch=st.number_input("Pitch(Inch)",min_value=0.0,value=4.0,max_value=10.0, step=0.1,format="%.1f")
        #angle_of_attack_deg = st.number_input("Propeller Angle of attack",min_value=0.0,value=7.7,max_value=89.9,step=0.1,format="%.1f")  

    with hub_and_counterweight_parameters:
       col1,col2,col3 = st.columns(3)
       with col1:
           hub_diam = st.number_input("Hub Diameter(mm)",min_value=3.0,value = 13.0,max_value=50.0,step=0.1,format="%.1f")
           hub_height = st.number_input("Hub Height(mm)",min_value=3.0,value = 7.0, max_value=50.0,step=0.1,format="%.1f")
           hub_hole_diam=st.number_input("Hub Hole Diameter(mm)",min_value=1.0,value=5.0,max_value=49.0,step=0.1,format="%.1f")
       with col2:
           hub_hole_sink_diam=st.number_input("Hub countersink Diameter(mm)",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_up_sink_depth=st.number_input("Hub countersink Upper Depth(mm)",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
           hub_hole_low_sink_depth=st.number_input("Hub countersink Lower Depth(mm)",min_value=0.01,value=0.01,max_value=50.0,step=0.25,format="%.2f")
       with col3:
           counterweight_length=st.number_input("Counterweight Length(mm)", min_value=10.0,value=17.0,max_value=50.0,step=0.1,format="%.1f")
           bolt_mm=st.number_input("Bolt Size(mm)",min_value=3,value=5,max_value=8)
           bolt_top_mm=st.number_input("Bolt Top thickness(mm)",min_value=2.0,value=3.5,max_value=8.0,step=0.1,format="%.1f")
           bolt_top_width_mm=st.number_input("Bolt Top Width(mm)",min_value=3.0,value=7.9,max_value=10.0,step=0.1,format="%.1f")

    with blade_parameters:
        chord_profile = st.selectbox('Chord Distribution',('parabolic','parabolic'))
        twist_profile = st.selectbox('Twist Profile',('exponential','linear'))
        num_of_sections=st.number_input("Number of Sections",min_value=1,value=250,max_value=500)
        blade_thickness=st.number_input("Blade Thickness Scale",min_value=0.1,value=1.1,max_value=5.0,step=0.1,format="%.1f")
        chord_scale=st.number_input("Chord Scale",min_value=0.01,value=0.15,max_value=0.25,step=0.01,format="%.2f")
        
        tip_size=st.number_input("Tip Size",min_value=0.01,value=7.0,max_value=20.0,step=0.1,format="%.1f")
        root_length=st.number_input("Root Length(mm)",min_value=0.5,value=10.0,max_value=30.0,step=0.1,format="%.1f")
        
    #propeller_diameter_mm = propeller_diameter_inch*25.4
    #angle_of_attack_deg = math.degrees(math.atan(pitch_inch / (math.pi * propeller_diameter_inch)))
    #chord_profile = 'parabolic'
    #twist_profile = 'exponential'
    
    return{
        'num_of_blades':num_of_blades,
        'propeller_diameter':propeller_diameter_inch*24.4,
        'angle_of_attack':math.degrees(math.atan(pitch_inch / (math.pi * propeller_diameter_inch))),
        'chord_scale':chord_scale,
        'tip_size':tip_size,
        'hub_diam':hub_diam,
        'hub_height':hub_height,
        'hub_hole_diam':hub_hole_diam,
        'hub_hole_sink_diam':hub_hole_sink_diam,
        'hub_hole_up_sink_depth':hub_hole_up_sink_depth,
        'hub_hole_low_sink_depth':hub_hole_low_sink_depth,
        'chord_profile':chord_profile,
        'root_length':root_length,
        'num_of_sections':num_of_sections,
        'blade_thickness':blade_thickness,
        'twist_profile':twist_profile,
        'counterweight_length':counterweight_length,
        'bolt_mm':bolt_mm,
        'bolt_top_mm':bolt_top_mm,
        'bolt_top_width_mm':bolt_top_width_mm
    }
