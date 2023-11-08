import streamlit as st

def make_scene(models):
    unions = ''

    scene_begin = f'''
scene = (
    cq.Workplane("XY")
    .union(model)
'''

    for index, params in enumerate(models):
        if params["layer_display"]:
            scene_begin = scene_begin + f'''    .union(model_{index})
'''
    return scene_begin +unions+ ')'

def layer_code(index, parameters):


    layer_string = f'''
 fart
'''
    return layer_string

def code_view(parameters, models):

    code_string = f'''
  
fart

'''

    if len(models) > 0:
        for index, layer_params in enumerate(models):
            layer_string = layer_code(index, layer_params)
            code_string = code_string + layer_string


    code_string = code_string + make_scene(models)

    code_string = code_string + '''
show_object(scene)
# cq.exporters.export(scene, 'obelisk.stl')
'''


    st.code(
    f'{code_string}',
    language="python", 
    line_numbers=True
)
