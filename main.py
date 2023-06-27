import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI_visual import create_window, section_names, param_input
import examples
import base_shapes
from base_shapes import shape_dict
from func_collection import func_dict, default_intervalls
from triangular_mesh import tri_mesh
from datetime import datetime

mayavi_imported = True
try:
    from mayavi import mlab
except ImportError:
    mayavi_imported = False



_VARS = {'window': False,
         'fig_agg': False,
         'plt_fig': False,
         'plt_ax': False}

_VARS['window'] = create_window()
_VARS['window'].maximize()

screen_dimensions = _VARS['window'].get_screen_size()


def get_plot_limits(data, pad=(0, 0)):
    ptp = np.ptp(data)
    left = min(data[:,0]) - pad[0] * ptp / 100
    right = max(data[:,0]) + pad[0] * ptp / 100
    top = min(data[:,0]) - pad[1] * ptp / 100
    bottom = max(data[:,0]) + pad[1] * ptp / 100
    return (left, right), (top, bottom)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def draw_base_chart():
    figsize = screen_dimensions[1] * 3 / 1080
    _VARS['plt_fig_base'] = plt.figure(figsize=2*[figsize], dpi=50, facecolor='black')
    _VARS['ax_base'] = _VARS['plt_fig_base'].add_subplot(111)
    _VARS['ax_base'].plot([])
    _VARS['ax_base'].set_axis_off()
    _VARS['ax_base'].set_facecolor('black')
    _VARS['plt_fig_base'].tight_layout()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'CHOICES-{section_names[0]}-Plot'].TKCanvas,\
        _VARS['plt_fig_base']
    )


def update_base_chart(base_shape):
    _VARS['fig_agg_base'].get_tk_widget().forget()
    _VARS['ax_base'].clear()

    polygon = Polygon(base_shape[:,:2], edgecolor='white', facecolor='black',\
                      linewidth=5)
    _VARS['ax_base'].add_patch(polygon)

    _VARS['ax_base'].set_xlim((-1.05, 1.05))
    _VARS['ax_base'].set_ylim((-1.05, 1.05))
    _VARS['ax_base'].set_facecolor('black')
    _VARS['ax_base'].set_aspect('equal')
    _VARS['ax_base'].set_axis_off()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'CHOICES-{section_names[0]}-Plot'].TKCanvas,\
        _VARS['plt_fig_base']
    )


def draw_path_chart():
    figsize = screen_dimensions[1] * 3 / 1080
    _VARS['plt_fig_path'] = plt.figure(figsize=2*[figsize], dpi=50, facecolor='black')
    _VARS['ax_path'] = _VARS['plt_fig_path'].add_subplot(111, projection='3d')
    _VARS['ax_path'].plot([], [], [])
    _VARS['ax_path'].set_axis_off()
    _VARS['ax_path'].set_facecolor('black')
    _VARS['plt_fig_path'].subplots_adjust(left=0, right=1, top=1, bottom=0)
    _VARS['fig_agg_path'] = draw_figure(
        _VARS['window'][f'CHOICES-{section_names[1]}-Plot'].TKCanvas, _VARS['plt_fig_path']
    )


def update_path_chart(path_func, start, end, num_steps):
    start, end = float(start), float(end)
    num_steps = int(num_steps)
    values = np.linspace(start, end, num_steps)
    func_values = np.array([path_func(value) for value in values])
    x, y, z = func_values.T
    _VARS['fig_agg_path'].get_tk_widget().forget()
    _VARS['ax_path'].clear()
    _VARS['ax_path'].set_axis_off()
    _VARS['ax_path'].set_facecolor('black')
    print(np.ptp(x), np.ptp(y), np.ptp(z))
    _VARS['ax_path'].set_box_aspect((np.ptp(x) + 1e-8, np.ptp(y) + 1e-8, np.ptp(z) + 1e-8))
    _VARS['ax_path'].plot(x, y, z, linewidth=4, color='white')
    _VARS['fig_agg_path'] = draw_figure(
        _VARS['window'][f'CHOICES-{section_names[1]}-Plot'].TKCanvas, _VARS['plt_fig_path']
    )



def draw_3d_chart():
    figsize = screen_dimensions[1]
    _VARS['plt_fig'] = plt.figure(figsize=2*[figsize], dpi=1, facecolor='black')
    _VARS['ax'] = _VARS['plt_fig'].add_subplot(111, projection='3d')
    _VARS['ax'].plot([], [], [])
    _VARS['ax'].set_axis_off()
    _VARS['ax'].set_facecolor('black')
    _VARS['plt_fig'].subplots_adjust(left=0, right=1, top=1, bottom=0)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['PREVIEW-Plot'].TKCanvas, _VARS['plt_fig']
    )


def update_3d_chart(x, y, z, triangles):
    _VARS['fig_agg'].get_tk_widget().forget()
    _VARS['ax'].clear()
    _VARS['ax'].set_axis_off()
    _VARS['ax'].set_facecolor('black')
    _VARS['ax'].set_box_aspect((np.ptp(x) + 1e-8, np.ptp(y) + 1e-8, np.ptp(z) + 1e-8))
    triang = mtri.Triangulation(x, y, triangles=triangles)
    _VARS['ax'].plot_trisurf(triang, z, cmap=plt.cm.rainbow,\
                             edgecolors='black', linewidths=8)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['PREVIEW-Plot'].TKCanvas, _VARS['plt_fig']
    )


def read_parameter(values):
    all_args = []
    for i, s in enumerate(section_names):
        if i == 2:
            continue
        args = []       
        for i in range(3):
            arg = values[f'INPUT-{i}-{s}']
            if arg:
                args.append(float(arg))
        func_section = values[f'COMBO-{s}']
        if s == section_names[0]:
            all_args.append(shape_dict[func_section](*args))
        elif s == section_names[1]:
            all_args.append(func_dict['p'][func_section](*args))
        elif s in section_names[3:5]:
            all_args.append(func_dict['s/r'][func_section](*args))
    all_args.append(float(values['INPUT-start']))
    all_args.append(float(values['INPUT-end']))
    all_args.append(int(values['INPUT-num_steps']))
    return tri_mesh(*all_args)
    

for s in section_names[:2]:
    for i in range(3):
        _VARS['window'][f'INPUT-{i}-{s}'].bind("<Return>", "-Enter")

_VARS['window'][f'INPUT-start'].bind("<Return>", "-Enter")
_VARS['window'][f'INPUT-end'].bind("<Return>", "-Enter")
_VARS['window'][f'INPUT-num_steps'].bind("<Return>", "-Enter")


draw_base_chart()
draw_path_chart()
draw_3d_chart()


for section in section_names:
    if section == section_names[0]:
        func = list(shape_dict.items())[0]
        update_base_chart(func[1]())
    elif section == section_names[1]:
        func = list(func_dict['p'].items())[0]
        for i, k in enumerate(('start', 'end', 'num_steps')):
            _VARS['window'][f'INPUT-{k}'].update(
                value=f'{default_intervalls[func[0]][i]}'
            )
        update_path_chart(func[1](), *default_intervalls[func[0]])
    elif section in section_names[3:5]:
        func = list(func_dict['s/r'].items())[0]
    else:
        continue
    args, defaults = param_input(*func)
    for i, arg in enumerate(args):
        _VARS['window'][f'INPUT-TEXT-{i}-{section}'].update(f'{arg}:')
        _VARS['window'][f'INPUT-{i}-{section}'].update(
            value=f'{defaults[i]}', background_color='#4d4d4d'
        )
    for k in range(len(args), 3):
        _VARS['window'][f'INPUT-TEXT-{k}-{section}'].update('')
        _VARS['window'][f'INPUT-{k}-{section}'].update(
            value='' ,background_color='black'
        )


while True:
    event, values = _VARS['window'].read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    print(event)
    print(values)
    print()

    if event.startswith('COMBO'):
        section = event[len('COMBO-'):]
        func_name = values[event]

        if section == section_names[0]:
            func = shape_dict[func_name]
            update_base_chart(func())

        elif section == section_names[1]:
            func = func_dict['p'][func_name]
            for i, k in enumerate(('start', 'end', 'num_steps')):
                _VARS['window'][f'INPUT-{k}'].update(
                    value=f'{default_intervalls[func_name][i]}'
                )
            update_path_chart(func(), *default_intervalls[func_name])

        elif section in section_names[3:5]:
            func = func_dict['s/r'][func_name]

        args, defaults = param_input(func_name, func)

        for i, arg in enumerate(args):
            _VARS['window'][f'INPUT-TEXT-{i}-{section}'].update(f'{arg}:')
            _VARS['window'][f'INPUT-{i}-{section}'].update(
                value=f'{defaults[i]}', background_color='#4d4d4d'
            )

        for k in range(len(args), 3):
            _VARS['window'][f'INPUT-TEXT-{k}-{section}'].update('')
            _VARS['window'][f'INPUT-{k}-{section}'].update(
                value='' ,background_color='black'
            )
        
    elif event.startswith('BUTTON'):
        action = event[len('BUTTON-'):]
        if action == 'preview':
            update_3d_chart(*read_parameter(values))
        elif mayavi_imported and (action == 'save'):
            mlab.options.offscreen = True
            mlab.triangular_mesh(*read_parameter(values))
            datetime_now = datetime.now()
            datetime_str = datetime_now.strftime("%Y_%m_%d_%H_%M_%S")
            mlab.savefig(datetime_str + ".obj")
    
    elif event.startswith('INPUT'):
        action = event.split('-')[-2]

        if action == 'Base':
            func = shape_dict[values['COMBO-Base']]
            args = []
            for i in range(3):
                arg = values[f'INPUT-{i}-Base']
                if arg != '':
                    args.append(arg)
            update_base_chart(func(*args))

        if action in ['Path', 'start', 'end', 'num_steps']:
            func = func_dict['p'][values['COMBO-Path']]
            func_args = []

            for i in range(3):
                func_arg = values[f'INPUT-{i}-Path']
                if func_arg != '':
                    func_args.append(func_arg)

            intervall_args = []
            for p in ['start', 'end', 'num_steps']:
                intervall_args.append(values[f'INPUT-{p}'])

            update_path_chart(func(*func_args), *intervall_args)


_VARS['window'].close()