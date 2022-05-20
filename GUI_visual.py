import PySimpleGUI as sg
from typing import Callable
from matplotlib.pyplot import margins
from func_collection import func_dict
from base_shapes import shape_dict
from inspect import getfullargspec

section_names = ('Base', 'Path', 'Scaling', 'Rotation', 'Intervall')


def param_input(func_name, func: Callable) -> dict:
    
    param_dict = getfullargspec(func)._asdict()

    return param_dict['args'], param_dict['defaults']


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
        s: [[sg.T(s, font=('fixed', 22), pad=(16, (10, 16))), sg.Push(),\
             sg.Combo(list_elements[s], key=f'COMBO-{s}', size=combo_size,\
                      default_value=list_elements[s][:1], enable_events=True,\
                      font=('fixed', 22), readonly=True, pad=(16, (10, 16)))]]
        for s in section_names[:4]
    }

    for s in section_names[:2]:
        choices_sections[s].append(
            [
            sg.Push(),
            sg.Column([
                [sg.Text(
                    '', key=f'INPUT-TEXT-{i}-{s}',
                    size=(10,1), pad=(0, 6), justification='right'
                ),
                sg.I(
                    key=f'INPUT-{i}-{s}', size=(5, 1),
                    justification='right', border_width=0, background_color='black'
                )]
                for i in range(3)
            ]),
            sg.Push(),
            sg.Column([[
                sg.Push(),
                sg.Canvas(key=f'CHOICES-{s}-Plot', pad=(6, 6)),
                sg.Push()
            ]]),
            sg.Push()
            ]
        )

    for s in section_names[2:4]:
        choices_sections[s].append([])
        for i in range(3):
            choices_sections[s][-1] += [
                sg.Text(
                    '', key=f'INPUT-TEXT-{i}-{s}', size=(10,1),
                    justification='right', border_width=0
                ),
                sg.Input(
                    key=f'INPUT-{i}-{s}', size=(5, 1), justification='right',
                    border_width=0, background_color='black'
                ),
                sg.Push()
            ]

    choices_sections[section_names[4]] = [
        [sg.T(section_names[4], font=('fixed', 22), pad=(16, (10, 16)))],
        [sg.Push(),
         sg.T('start:'), sg.I(default_text='0', size=(5, 1), key='INPUT-start', justification='right', border_width=0),
         sg.Push(),
         sg.T('end:'),sg.I(default_text='1', size=(5, 1), key='INPUT-end', justification='right', border_width=0),
         sg.Push(),
         sg.T('num_steps:'), sg.I(default_text='20', size=(5, 1), key='INPUT-num_steps', justification='right', border_width=0),
         sg.Push()]
    ]

    choices_column = [
        [sg.Frame('', choices_sections[s], key=f'CHOICES-Column-{s}',\
                   expand_y=True, expand_x=True, border_width=4)]
        for s in section_names
    ]

    choices_column.append(
        [sg.Push(),
         sg.B('show', key='BUTTON-preview', size=(14, 1), pad=(0, (16,0))),\
         sg.Push(),]
    )

    preview_column = [
        [sg.Push(), sg.Canvas(key='PREVIEW-Plot'), sg.Push()]
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