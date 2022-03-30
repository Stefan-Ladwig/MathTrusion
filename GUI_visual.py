import PySimpleGUI as sg
from matplotlib.pyplot import margins
from func_collection import func_dict
from base_shapes import shape_dict

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

section_names = ['Base', 'Path', 'Scaling', 'Rotation', 'Intervall']


def listbox_size(string_list):
    width = max(map(len, string_list))
    height = len(string_list)
    return (width + 2, height)


def create_window():
    sg.theme('Black')

    list_elements = {
        section_names[0]: list(shape_dict.keys()),
        section_names[1]: list(func_dict['p'].keys()),
        section_names[2]: list(func_dict['s/r'].keys()),
        section_names[3]: list(func_dict['s/r'].keys()),
    }

    select_section = {
        s:[
            [sg.Combo(list_elements[s], key=f'-{s}-', \
                      size=listbox_size(list_elements[s]),\
                      default_value=list_elements[s][:1],\
                      font=('fixed', 15), readonly=True)],
            [sg.B('Select', key=f'-SELECT SEC{s}')]
        ]
        for s in section_names[:4]
    }
    select_section[section_names[4]] = [
        [sg.T('start')],
        [sg.I(size=(10, 1), key='-SELECT start-')],
        [sg.T('stop')],
        [sg.I(size=(10, 1), key='-SELECT end-')],
        [sg.T('number of steps')],
        [sg.I(size=(10, 1), key='-SELECT num_steps-')],
        [sg.B('Select', key=f'-SELECT {section_names[4]}')]
    ]

    select_column = []
    for s in section_names:
        select_column.append(
            [sg.T(SYMBOL_DOWN, enable_events=True, k=f'-OPEN SEC{s}-'),\
             sg.T(f'{s}', enable_events=True,\
                  k=f'-OPEN SEC{s}-TEXT', font=('fixed', 26))]
        )
        select_column.append(
            [sg.pin(sg.Column(select_section[s], key=f'-SEC{s}-'))]
        )

    choices_column = [
        [sg.Push(), sg.T(section_names[0]), sg.Push()],
        [sg.T('', key=f'-CHOICES {section_names[0]} Name-')],
        [sg.Push(), sg.Canvas(key=f'-CHOICES {section_names[0]} Plot-'),\
         sg.Push()]
        ,
        [sg.Push(), sg.T(section_names[1]), sg.Push()],
        [sg.T('', key=f'-CHOICES {section_names[1]} Name-')],
        [sg.T('function here',\
            key=f'-CHOICES {section_names[1]} function-')]
        ,
        [sg.Push(), sg.T(section_names[2]), sg.Push()],
        [sg.T('', key=f'-CHOICES {section_names[2]} Name')],
        [sg.T('function here',\
            key=f'-CHOICES {section_names[2]} function-')]
        ,
        [sg.Push(), sg.T(section_names[3]), sg.Push()],
        [sg.T('', key=f'-CHOICES {section_names[3]} Name')],
        [sg.T('function here',\
            key=f'CHOICES {section_names[3]} function-')]
        ,
        [sg.Push(), sg.T(section_names[4]), sg.Push()],
        [sg.T('start, stop, num_steps',\
            key=f'-CHOICES {section_names[4]}-')]
    ]

    preview_column = [
        [sg.Push(), sg.T('Preview', font=('fixed', 26)), sg.Push()],
        [sg.Push(), sg.Canvas(key='-PREVIEW Plot-'), sg.Push()],
        [sg.Push(), sg.B('Create Modell', key='-PREVIEW Button-'), sg.Push()]
    ]

    layout = [
        [
            sg.Column(select_column, vertical_alignment='top',\
                      expand_y=True, expand_x=True,\
                      pad=(10,6)),
            sg.VSeperator(),
            sg.Column(choices_column,\
                      expand_y=True, expand_x=True,\
                      pad=(10,6)),
            sg.VSeparator(),
            sg.Column(preview_column,\
                      expand_y=True, expand_x=True,\
                      pad=(20,6)),
        ]
    ]
    
    return sg.Window('Visible / Invisible Element Demo', layout,\
                     finalize=True, resizable=True, font=('fixed', 16))