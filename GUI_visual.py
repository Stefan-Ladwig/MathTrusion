import PySimpleGUI as sg
from matplotlib.pyplot import margins
from func_collection import func_dict
from base_shapes import shape_dict

section_names = ['Base', 'Path', 'Scaling', 'Rotation', 'Intervall']


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
        s: [[sg.T(s, font=('fixed', 22), pad=(0, 16)), sg.Push(),\
             sg.Combo(list_elements[s], key=f'-{s}-', size=combo_size,\
                      default_value=list_elements[s][:1], enable_events=True,\
                      font=('fixed', 22), readonly=True)]]
        for s in section_names[:4]
    }

    choices_sections[section_names[0]].append(
        [sg.Push(),
         sg.Canvas(key=f'-CHOICES {section_names[0]} Plot-', pad=(6, 6)),
         sg.Push()]
    )

    choices_sections[section_names[4]] = [
        [sg.Text(section_names[4], font=('fixed', 22), pad=(0, 14))],
        [sg.T('start'), sg.Push(), sg.I(size=(10, 1), key='-SELECT start-')],
        [sg.T('end'), sg.Push(), sg.I(size=(10, 1), key='-SELECT end-')],
        [sg.T('number of steps'), sg.Push(), sg.I(size=(10, 1),\
         key='-SELECT num_steps-')]
    ]

    choices_column = [
        [sg.Column(choices_sections[s], key=f'-CHOICES Column {s}-',\
                   expand_y=True, expand_x=True)]
        for s in section_names
    ]

    choices_column.append(
        [sg.Push(), sg.B('preview', key='-BUTTON preview-', size=(14, 1)),\
         sg.Push(), sg.B('save', key='-BUTTON create-', size=(14, 1)), sg.Push(),\
         sg.Push(), sg.B('view in mayavi', key='-BUTTON mayavi-', size=(14, 1)), sg.Push()]
    )

    preview_column = [
        [sg.Push(), sg.Canvas(key='-PREVIEW Plot-'), sg.Push()]
    ]

    layout = [
        [
            sg.Column(choices_column,\
                      expand_y=True, expand_x=True,\
                      pad=((10, 60),(0, 6))),
            sg.VSeparator(),
            sg.Column(preview_column,\
                      expand_y=True, expand_x=True,\
                      pad=(20,0)),
        ]
    ]
    
    return sg.Window('Visible / Invisible Element Demo', layout,\
                     finalize=True, resizable=True, font=('fixed', 16))