import PySimpleGUI as sg
from typing import Callable
from matplotlib.pyplot import margins
from func_collection import func_dict
from base_shapes import shape_dict
from inspect import getfullargspec

section_names = ('Base', 'Path', 'Scaling', 'Rotation', 'Intervall')


def param_input_layout(func_name, func: Callable) -> list:
    param_dict = getfullargspec(func)._asdict()
    layout = [sg.Push()]
    for i, arg in enumerate(param_dict['args']):
        layout += [
            sg.T(f'{arg}:'), sg.I(key=f'{func_name}: {arg}', size=(6, 1),\
            default_text='{}'.format(param_dict['defaults'][i]),\
            justification='right'),\
            sg.Push()
        ]
    return [layout]


def create_window():
    sg.theme('Black')

    list_elements = {
        section_names[0]: list(shape_dict.keys()),
        section_names[1]: list(func_dict['p'].keys()),
        section_names[2]: list(func_dict['s/r'].keys()),
        section_names[3]: list(func_dict['s/r'].keys()),
    }

    combo_size = 0
    for e in list_elements.values():
        longest_str = max(map(len, e))
        if longest_str > combo_size:
            combo_size = longest_str
    combo_size += 1

    choices_sections = {
        s: [[sg.T(s, font=('fixed', 22), pad=16), sg.Push(),\
             sg.Combo(list_elements[s], key=f'-COMBO {s}-', size=combo_size,\
                      default_value=list_elements[s][:1], enable_events=True,\
                      font=('fixed', 22), readonly=True, pad=16)]]
        for s in section_names[:4]
    }

    choices_sections[section_names[0]].append(
        [sg.Push(),
         sg.Canvas(key=f'-CHOICES {section_names[0]} Plot-', pad=(6, 6)),
         sg.Push()]
    )

    choices_sections[section_names[4]] = [
        [sg.Text(section_names[4], font=('fixed', 22), pad=16)],
        [sg.Push(),
         sg.T('start:'), sg.I(size=(6, 1), key='-SELECT start-'),
         sg.Push(),
         sg.T('end:'),sg.I(size=(6, 1), key='-SELECT end-'),
         sg.Push(),
         sg.T('number of steps:'), sg.I(size=(6, 1), key='-SELECT num_steps-'),
         sg.Push()]
    ]

    choices_column = [
        [sg.Frame('', choices_sections[s], key=f'-CHOICES Column {s}-',\
                   expand_y=True, expand_x=True, border_width=4)]
        for s in section_names
    ]

    choices_column.append(
        [sg.Push(), sg.B('preview', key='-BUTTON preview-', size=(14, 1), pad=(0, (16,0))),\
         sg.Push(), sg.B('save', key='-BUTTON create-', size=(14, 1), pad=(0, (16,0))),\
         sg.Push(), sg.B('view in mayavi', key='-BUTTON mayavi-', size=(14, 1), pad=(0, (16,0))), sg.Push()]
    )

    preview_column = [
        [sg.Push(), sg.Canvas(key='-PREVIEW Plot-'), sg.Push()]
    ]

    layout = [
        [
            sg.Column(choices_column,\
                      expand_y=True, expand_x=True,\
                      pad=((10, 60),(0, 6))),
            sg.Column(preview_column,\
                      expand_y=True, expand_x=True,\
                      pad=(20,0)),
        ]
    ]
    
    return sg.Window('Visible / Invisible Element Demo', layout,\
                     finalize=True, resizable=True, font=('fixed', 16))