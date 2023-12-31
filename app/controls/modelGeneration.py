import streamlit as st
import cadquery as cq
import math

def generate_hub_multi(parameters):
    # Set up a new workplane centered on the XY plane
    hub_multi_wp = (cq.Workplane("XY")
        # Make a cylinder as the main body, with a height and a radius        
        .cylinder(
            parameters['hub_height'],
            parameters['hub_diam']/2)
        # Select the top face
        .faces(">Z")
        # Cut a hole through the cylinder along the Z-axis with a specified diameter
        .hole(parameters['hub_hole_diam'])
        # Select the top face again
        .faces(">Z")
        # Cut another hole as the top countersink, with specified diameter and depth
        .hole(
            parameters['hub_hole_sink_diam'],
            parameters['hub_hole_up_sink_depth'])
        # Select the bottom face
        .faces("<Z")
        # Create a new workplane to center
        .workplane()
        # Cut the bottom countersink
        .hole(
            parameters['hub_hole_sink_diam'],
            parameters['hub_hole_low_sink_depth'])
        # Translate the hub to a correct position in the 3D-space
        .translate((0,0,parameters['hub_height']/2))
        )
    # Return the hub as an object on the workplane
    return hub_multi_wp

def generate_counterweighted_hub(parameters):
    # Set up a new workplane centered on the XY plane
    hub_wp= (cq.Workplane("XY")
        # Make a box as the main body, with a length, width and height  
        .box(
            parameters['hub_diam']+parameters['counterweight_length'],
            parameters['hub_diam'],
            parameters['hub_height'])
        # Select the vertical edges and fillet them
        .edges("|Z")
        .fillet(
            parameters['hub_diam']/2.5)
        # Move the box a little to the along the Z-axis
        .translate((0,0,parameters['hub_height']/2))
        # Select the top face to make a hole for the shaft
        .faces(">Z")
        .center(((parameters['hub_diam']+parameters['counterweight_length']/2)-parameters['hub_diam']),0)
        .circle(parameters['hub_hole_diam']/2)
        .cutBlind(parameters['hub_height'])
        # Make a countersink on the top face
        .faces(">Z")
        .workplane()
        .circle(parameters['hub_hole_sink_diam']/2)
        .cutBlind(-parameters['hub_hole_up_sink_depth'])
        # Make a countersink on the bottom face
        .faces("<Z")
        .workplane()
        .circle(parameters['hub_hole_sink_diam']/2)
        .cutBlind(-parameters['hub_hole_low_sink_depth'])
        )

    # Make a bolt hole through the counterweight
    counterweighted_hub_wp = (hub_wp
        .faces(">Z")
        .center(-((parameters['hub_diam']+parameters['counterweight_length']/2)-parameters['hub_diam'])*2,0)
        .circle(parameters['bolt_mm']/2)
        .cutBlind(-parameters['hub_height'])
        # Create a square countersink on the bottom face where the bolt head will fit
        .faces("<Z")
        .workplane()
        .rect(
            parameters['bolt_top_width_mm']*1.05,
            parameters['bolt_top_width_mm']*1.05)
        .cutBlind(-parameters['bolt_top_mm'])
        )

    # Move the counterweight to it's proper position
    counterweighted_hub_wp = (cq.Workplane("XY")
        .add(counterweighted_hub_wp)
        .translate((-((parameters['hub_diam']+parameters['counterweight_length']/2)-parameters['hub_diam']),0,0))
        )

    # Return the hub as an object on the workplane
    return counterweighted_hub_wp  

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
    airfoil_points= [(1.0, 0.00), (0.95, 0.0134), (0.9, 0.0245), (0.8, 0.0441), (0.7, 0.061), (0.6, 0.075), (0.5, 0.0857), (0.4, 0.0925), (0.3, 0.0938), (0.25, 0.0917), (0.2, 0.087), (0.15, 0.0797), (0.1, 0.0683), (0.075, 0.0606), (0.05, 0.0507), (0.025, 0.0371), (0.0125, 0.0271), (0.0, 0.0), (0.0125, -0.0206), (0.025, -0.0286), (0.05, -0.0384), (0.075, -0.0447), (0.1, -0.049), (0.15, -0.0542), (0.2, -0.0566), (0.25, -0.057), (0.3, -0.0562), (0.4, -0.0525), (0.5, -0.0467), (0.6, -0.039), (0.7, -0.0305), (0.8, -0.0215), (0.9, -0.0117), (0.95, -0.0068), (1.0, -0.00)]
    
    return airfoil_points

def scale_airfoil_points(airfoil_points,chord, scale_x, scale_y):
    center_x=sum(x for x,_ in airfoil_points)/len(airfoil_points)
    center_y=sum(y for _,y in airfoil_points)/len(airfoil_points)
    trans_points = [(x-center_x,y-center_y)for x,y in airfoil_points]
    
    scale_factor = chord/(2*max(abs(x)for x,_ in trans_points))
    scaled_points = [(x*scale_factor* scale_x,y*scale_factor*scale_y)for x,y in trans_points]

    scaled_airfoil_points =[(x,-y)for x,y in scaled_points]
    
    return scaled_airfoil_points

def twist_angle_linear(r, parameters):
    return parameters['angle_of_attack']+math.degrees(math.atan(2*((parameters['propeller_diameter']/2)-r)/parameters['propeller_diameter']))

def twist_angle_exponential(r,parameters):
    blade_length = (parameters['propeller_diameter'] / 2) - (parameters['root_length']*2) - (parameters['hub_diam'] / 2)
    decrease_factor = 2
    twist_angle = (90 - parameters['angle_of_attack']) * math.exp(-decrease_factor * (r / blade_length)) + parameters['angle_of_attack']
    return twist_angle

def elliptic_chord(r, parameters):
    chord = ((parameters['propeller_diameter'] * parameters['chord_scale']) * math.sqrt(1 - (r / (parameters['propeller_diameter']/2))**2))+parameters['tip_size']
    return max(chord, parameters['tip_size'])

def parabolic_chord(r,parameters):
    blade_length = parameters['propeller_diameter'] / 2
    max_chord = (parameters['chord_scale'] * parameters['propeller_diameter'])
    chord = max(min(((parameters['tip_size'] - max_chord) / ((blade_length - (blade_length / 2))**2) * (r - (blade_length / 2))**2 + max_chord), max_chord), 0)
    if r == blade_length:
        chord = max(chord, parameters['tip_size'])
    return chord

def generate_blade(parameters):
    # Set parameters
    airfoil_points = get_airfoil_points() # Get the airfoil points, currently set to NACA2415
    blade_length = (parameters['propeller_diameter'] / 2) - (parameters['root_length']) - (parameters['hub_diam'] / 2) # Calculate blade lenght
    segment_length = blade_length/parameters['num_of_sections'] # Calculate length of each segment
    offsets = ([parameters['root_length']+ i * segment_length for i in range(0, parameters['num_of_sections'] + 1)]) # Calculate offset for each section
    # Start a list for the splines
    airfoil_splines = {}
    # Get the twist angle at the root, depending on selected profile, more can be added
    r = (parameters['hub_diam']/2)
    if parameters['twist_profile'] == 'linear':
        twist_angle = twist_angle_linear(r, parameters)
        twist_angle_set = 'linear'
    elif parameters['twist_profile'] == 'exponential':
        twist_angle = twist_angle_exponential(r,parameters) 
        twist_angle_set = 'exponential'
    # Create the spline for the root, fitting in the hub height
    airfoil_splines["airfoil_points_{}".format(0)]=(cq.Workplane("XY")
        .workplane(offset=0)
        .transformed(rotate=(0,0,twist_angle))
        .spline(scale_airfoil_points(airfoil_points,1.5*parameters['hub_height'],0.6,6))
        .close()
        .wire()
        .val())
    i=1
    # Iterate over the sections to create their splines
    for offset in offsets:
        r = (parameters['hub_diam']/2)+offset
        # Find the twist angle for the current section
        if twist_angle_set == 'linear':
            twist_angle = twist_angle_linear(r, parameters)
        elif twist_angle_set == 'exponential':
            twist_angle = twist_angle_exponential(r,parameters)
        # Find chord length for current section
        if parameters['chord_profile'] == 'elliptic':
            chord = elliptic_chord(r, parameters)
        elif parameters['chord_profile'] == 'parabolic':
            chord = parabolic_chord(r,parameters)
        # Scale the airfoil points for the current section
        scaled_airfoil_points = scale_airfoil_points(airfoil_points,chord,1,parameters['blade_thickness'])
        # Create the spline for the curreent section
        wp=(cq.Workplane("XY")
            .workplane(offset=offset)
            .transformed(rotate=(0,0,twist_angle))
            .spline(scaled_airfoil_points)
            .close()
            .wire()
            .val())
        # Add the section spline to the list
        airfoil_splines["airfoil_points_{}".format(i)]= wp
        i = i+1
    # Create a lofted solid between all sections
    sections = list(airfoil_splines.values())
    loft = cq.Solid.makeLoft(sections).Faces()
    shell = cq.Shell.makeShell(loft)
    blade = cq.Solid.makeSolid(shell)
    # Create a workplane for the blade
    blade_wp = cq.Workplane("XY").add(blade)
    # Extrude the root a little into the hub
    extrusion_depth = -((parameters['hub_diam']/2)-max((parameters['hub_hole_diam']/2),(parameters['hub_hole_sink_diam']/2)))
    base_wire = blade_wp.faces("<Z").wires().vals()[0]
    extrusion = (cq.Workplane("XY")
             .add(base_wire)
             .toPending()
             .extrude(extrusion_depth))
    # Add this extruded root to the main blade
    blade_wp  = blade_wp.union(extrusion)
    # Return the blade as a workplane object
    return blade_wp

def generate_propeller(parameters):
    # Choose hub type based on the number of blades
    if parameters['num_of_blades'] == 1:
        counterweighted_hub_wp=generate_counterweighted_hub(parameters)
        propeller = cq.Workplane("XY").add(counterweighted_hub_wp)
    else:
        hub_multi_wp=generate_hub_multi(parameters)
        propeller = cq.Workplane("XY").add(hub_multi_wp)
    # Generate a workplane for the blade
    blade_wp = generate_blade(parameters)
    hub_radius = parameters['hub_diam']/2
    # Iterate over the number of blades and place them on the hub
    for i in range(parameters['num_of_blades']):
        # Find the angle for each blade
        angle = i*(360/parameters['num_of_blades'])
        # Find the position for each blade
        x_pos = (hub_radius-(hub_radius*0.0))*math.cos(math.radians(angle))
        y_pos = (hub_radius-(hub_radius*0.0))*math.sin(math.radians(angle))
        # Orient and position the blade on the hub
        blade = (blade_wp
                 .rotate((0, 0, 0), (0, 0, 1), 180)
                 .rotate((0, 0, 0), (0, 1, 0), 90)
                 .rotate((0, 0, 0), (1, 0, 0), 90)
                 .rotate((0, 0, 0), (0, 0, 1), angle)
                 .translate((x_pos,y_pos,parameters['hub_height']/2)))
        # Add the blade to the propeller
        propeller = propeller.union(blade)
    # Return the completed propeller
    return propeller
