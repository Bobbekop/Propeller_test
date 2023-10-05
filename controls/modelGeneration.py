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
    if global_airfoil_file_path is None:
        global_airfoil_file_path=filedialog.askopenfilename(filetypes=[("Dat Files","*.dat")])
    """
    airfoil_file= global_airfoil_file
    
    airfoil_points=[]
    
    if airfoil_file is not None:
        file_content = uploaded_file.read().decode()
        lines=file_content.split("\n")
        for line in lines[1:]:
            if line:
                x,y = map(float,line.split())
                airfoil_points.append((x,y))
    
    return airfoil_points

def scale_airfoil_points(airfoil_points,chord,parameters):

    center_x=sum(x for x,_ in airfoil_points)/len(airfoil_points)
    center_y=sum(y for _,y in airfoil_points)/len(airfoil_points)
    trans_points = [(x-center_x,y-center_y)for x,y in airfoil_points]
    
    scale_factor = chord/(2*max(abs(x)for x,_ in trans_points))
    scaled_points = [(x*scale_factor,y*scale_factor)for x,y in trans_points]
    
    #desired_center_x = 0.0
    #desired_center_y = 0.0
    #scaled_airfoil_points = [(x+ desired_center_x,y + desired_center_y)for x,y in scaled_points]
    scaled_airfoil_points =[(x,-y)for x,y in scaled_points]
    
    return scaled_airfoil_points

def compute_blade_length(parameters):
    return (parameters['propeller_diameter'] / 2) - (parameters['root_length']) - (parameters['hub_diam'] / 2)

def compute_twist_angle(r, parameters):
    return parameters['angle_of_attack']+math.degrees(math.atan(2*((parameters['propeller_diameter']/2)-r)/parameters['propeller_diameter']))

def elliptical_chord(r,parameters):
    r = min(r, (parameters['propeller_diameter'] / 2) - parameters['tip_size'])
    return (parameters['propeller_diameter'] * parameters['chord_scale']) * math.sqrt(1 - (r/(parameters['propeller_diameter'] / 2))**2)

def generate_blade(parameters):

    airfoil_points = get_airfoil_points()
    
    base_wp = cq.Workplane("XY")
    
    blade_length = compute_blade_length(parameters)
    segment_length = blade_length/parameters['num_of_sections']
    
    offsets = ([parameters['root_length']+ i * segment_length for i in range(0, parameters['num_of_sections'] + 1)])
    
    airfoil_splines = {}
    
    airfoil_splines["airfoil_points_{}".format(0)]=(base_wp
        .workplane(offset=0)
        .transformed(rotate=(0,0,90))
        .spline(scale_airfoil_points(airfoil_points,parameters['hub_height'],parameters))
        .close()
        .wire()
        .val())
    
    i=1

    for offset in offsets:
        r = (parameters['hub_diam']/2)+offset
        twist_angle=compute_twist_angle(r,parameters)
        chord=elliptical_chord(r,parameters)
        scaled_airfoil_points = scale_airfoil_points(airfoil_points,chord,parameters)
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
    
    return blade_wp

def generate_propeller(hub_wp,blade_wp,parameters):
    
    propeller = cq.Workplane("XY").add(hub_wp)
    hub_radius = parameters['hub_diam']/2
    
    for i in range(parameters['num_of_blades']):
        angle = i*(360/parameters['num_of_blades'])
        x_pos = (hub_radius-(hub_radius*0.05))*math.cos(math.radians(angle))
        y_pos = (hub_radius-(hub_radius*0.05))*math.sin(math.radians(angle))
        
        blade = (blade_wp
                 .rotate((0, 0, 0), (0, 0, 1), 180)
                 .rotate((0, 0, 0), (0, 1, 0), 90)
                 .rotate((0, 0, 0), (1, 0, 0), 90)
                 .rotate((0, 0, 0), (0, 0, 1), angle)
                 .translate((x_pos,y_pos,parameters['hub_height']/2)))
        
        propeller = propeller.union(blade)
    
    return propeller
