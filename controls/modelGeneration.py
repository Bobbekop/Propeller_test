import streamlit as st
import cadquery as cq
import math
import tkinter as tk
from tkinter import filedialog

global_airfoil_file = None

def generate_hub(parameters):
    hub_wp = (cq.Workplane("XY")
        .cylinder(
            parameters['hub_height'],
            parameters['hub_diam']/2)
        .faces(">Z")
        .hole(
            parameters['hub_hole_diam'])
        .faces(">Z")
        .hole(parameters['hub_hole_chamf_diam'],parameters['hub_hole_up_chamf_depth'])
        .faces("<Z")
        .circle((parameters['hub_hole_chamf_diam']/2))
        .cutBlind(parameters['hub_hole_low_chamf_depth'])
        .translate((0,0,parameters['hub_height']/2)))
    
    return hub_wp

def get_airfoil_points():
    """
    global global_airfoil_file_path
    
    if global_airfoil_file_path is None:
        global_airfoil_file_path=filedialog.askopenfilename(filetypes=[("Dat Files","*.dat")])
    
    airfoil_file_path= global_airfoil_file_path
    
    airfoil_points=[]
    
    if airfoil_file_path:
        with open(airfoil_file_path,'r')as file:
            skip_first_line=True
            for line in file:
                if skip_first_line:
                    skip_first_line = False
                    continue
                values=line.strip().split()
                if len(values)>=2:
                    x=float(values[0])
                    y=float(values[1])
                    airfoil_points.append((x,y))
        if not airfoil_points:
            global_airfoil_file_path = None
            print("Something is wrong with the file.")
    
    #log(airfoil_points)
    """
    airfoil_points= [(1.0, 0.0016), (0.95, 0.0134), (0.9, 0.0245), (0.8, 0.0441), (0.7, 0.061), (0.6, 0.075), (0.5, 0.0857), (0.4, 0.0925), (0.3, 0.0938), (0.25, 0.0917), (0.2, 0.087), (0.15, 0.0797), (0.1, 0.0683), (0.075, 0.0606), (0.05, 0.0507), (0.025, 0.0371), (0.0125, 0.0271), (0.0, 0.0), (0.0125, -0.0206), (0.025, -0.0286), (0.05, -0.0384), (0.075, -0.0447), (0.1, -0.049), (0.15, -0.0542), (0.2, -0.0566), (0.25, -0.057), (0.3, -0.0562), (0.4, -0.0525), (0.5, -0.0467), (0.6, -0.039), (0.7, -0.0305), (0.8, -0.0215), (0.9, -0.0117), (0.95, -0.0068), (1.0, -0.0016)]
    
    return airfoil_points

def scale_airfoil_points(airfoil_points,chord, scale_x, scale_y):
    center_x=sum(x for x,_ in airfoil_points)/len(airfoil_points)
    center_y=sum(y for _,y in airfoil_points)/len(airfoil_points)
    trans_points = [(x-center_x,y-center_y)for x,y in airfoil_points]
    
    scale_factor = chord/(2*max(abs(x)for x,_ in trans_points))
    scaled_points = [(x*scale_factor* scale_x,y*scale_factor*scale_y)for x,y in trans_points]
    
    #desired_center_x = 0.0
    #desired_center_y = 0.0
    #scaled_airfoil_points = [(x+ desired_center_x,y + desired_center_y)for x,y in scaled_points]
    scaled_airfoil_points =[(x,-y)for x,y in scaled_points]
    
    return scaled_airfoil_points

def compute_blade_length(parameters):
    return (parameters['propeller_diameter'] / 2) - (parameters['root_length']) - (parameters['hub_diam'] / 2)

def compute_twist_angle(r, parameters):
    return parameters['angle_of_attack']+math.degrees(math.atan(2*((parameters['propeller_diameter']/2)-r)/parameters['propeller_diameter']))

def elliptical_chord(r, parameters):
    chord = (parameters['propeller_diameter'] * parameters['chord_scale']) * math.sqrt(1 - (r / (parameters['propeller_diameter'] / 2))**2)
    return max(chord, parameters['tip_size'])

def generate_blade(parameters):
    airfoil_points = get_airfoil_points()
    
    base_wp = cq.Workplane("XY")
    
    blade_length = compute_blade_length(parameters)
    segment_length = blade_length/parameters['num_of_sections']
    
    offsets = ([parameters['root_length']+ i * segment_length for i in range(0, parameters['num_of_sections'] + 1)])
    
    airfoil_splines = {}
    
    r = (parameters['hub_diam']/2)
    twist_angle=compute_twist_angle(r,parameters)
    airfoil_splines["airfoil_points_{}".format(0)]=(base_wp
        .workplane(offset=0)
        .transformed(rotate=(0,0,twist_angle))
        .spline(scale_airfoil_points(airfoil_points,1.5*parameters['hub_height'],0.75,5))
        .close()
        .wire()
        .val())
    
    i=1

    for offset in offsets:
        r = (parameters['hub_diam']/2)+offset
        twist_angle=compute_twist_angle(r,parameters)
        chord=elliptical_chord(r,parameters)
        scaled_airfoil_points = scale_airfoil_points(airfoil_points,chord,1,parameters['blade_thickness'])
        wp=(base_wp
            .workplane(offset=offset)
            .transformed(rotate=(0,0,twist_angle))
            .spline(scaled_airfoil_points)
            .close()
            .wire()
            .val())
        
        airfoil_splines["airfoil_points_{}".format(i)]= wp
        i = i+1
    
    sections = list(airfoil_splines.values())
    
    loft = cq.Solid.makeLoft(sections).Faces()
    shell = cq.Shell.makeShell(loft)
    blade = cq.Solid.makeSolid(shell)
    
    blade_wp = cq.Workplane("XY").add(blade)
    extrusion_depth = -((parameters['hub_diam']/2)-(parameters['hub_hole_diam']/2))
    base_wire = blade_wp.faces("<Z").wires().vals()[0]
    extrusion = (cq.Workplane("XY")
             .add(base_wire)
             .toPending()
             .extrude(extrusion_depth))
    blade_wp  = blade_wp.union(extrusion)
    
    return blade_wp

def generate_propeller(parameters):
    if parameters['num_of_blades'] == 1:
        counterweighted_hub_wp=generate_counterweighted_hub(parameters)
        propeller = cq.Workplane("XY").add(counterweighted_hub_wp)
    else:
        hub_wp=generate_hub(parameters)
        propeller = cq.Workplane("XY").add(hub_wp)

    blade_wp = generate_blade(parameters)
    hub_radius = parameters['hub_diam']/2
    
    for i in range(parameters['num_of_blades']):
        angle = i*(360/parameters['num_of_blades'])
        x_pos = (hub_radius-(hub_radius*0.0))*math.cos(math.radians(angle))
        y_pos = (hub_radius-(hub_radius*0.0))*math.sin(math.radians(angle))
        
        blade = (blade_wp
                 .rotate((0, 0, 0), (0, 0, 1), 180+angle)
                 .rotate((0, 0, 0), (0, 1, 0), 90)
                 .rotate((0, 0, 0), (1, 0, 0), 90)
                 .translate((x_pos,y_pos,parameters['hub_height']/2)))
        
        propeller = propeller.union(blade)
    
    return propeller
