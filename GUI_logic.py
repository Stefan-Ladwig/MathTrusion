import PySimpleGUI as sg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI_visual import create_window, section_names, param_input_layout
import examples
import base_shapes
from matplotlib.patches import Polygon
from base_shapes import shape_dict
from func_collection import func_dict


_VARS = {'window': False,
         'fig_agg': False,
         'plt_fig': False,
         'plt_ax': False}

_VARS['window'] = create_window()
_VARS['window'].maximize()

screen_dimensions = sg.Window.get_screen_size()


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
    figsize = screen_dimensions[1] * 5 / 1080
    _VARS['plt_fig_base'] = plt.figure(figsize=2*[figsize], dpi=50, facecolor='black')
    _VARS['ax_base'] = _VARS['plt_fig_base'].add_subplot(111)
    _VARS['ax_base'].plot([])
    _VARS['ax_base'].set_axis_off()
    _VARS['ax_base'].set_facecolor('black')
    _VARS['plt_fig_base'].tight_layout()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'-CHOICES {section_names[0]} Plot-'].TKCanvas,\
        _VARS['plt_fig_base']
    )


def update_base_chart(base_shape):
    _VARS['fig_agg_base'].get_tk_widget().forget()
    _VARS['ax_base'].clear()

    polygon = Polygon(base_shape[:,:2], edgecolor='white', facecolor='black',\
                      linewidth=5)
    _VARS['ax_base'].add_patch(polygon)

    xlim, ylim = get_plot_limits(base_shape, (4, 4))
    _VARS['ax_base'].set_xlim(xlim)
    _VARS['ax_base'].set_ylim(ylim)
    _VARS['ax_base'].set_facecolor('black')
    _VARS['ax_base'].set_aspect('equal')
    _VARS['ax_base'].set_axis_off()
    _VARS['fig_agg_base'] = draw_figure(
        _VARS['window'][f'-CHOICES {section_names[0]} Plot-'].TKCanvas,\
        _VARS['plt_fig_base']
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
        _VARS['window']['-PREVIEW Plot-'].TKCanvas, _VARS['plt_fig']
    )


def update_3d_chart(x, y, z, triangles):
    _VARS['fig_agg'].get_tk_widget().forget()
    _VARS['ax'].clear()
    _VARS['ax'].set_axis_off()
    _VARS['ax'].set_facecolor('black')
    _VARS['ax'].set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
    triang = mtri.Triangulation(x, y, triangles=triangles)
    _VARS['ax'].plot_trisurf(triang, z, cmap=plt.cm.rainbow,\
                             edgecolors='grey', linewidths=0.1)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['-PREVIEW Plot-'].TKCanvas, _VARS['plt_fig']
    )


draw_base_chart()
update_base_chart(base_shapes.n_gon(5))
draw_3d_chart()
update_3d_chart(*examples.mobius_loop())


while True:
    event, values = _VARS['window'].read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    print(event)
    print(values)
    print()

    if event.startswith('-COMBO'):
        section = event[len('-COMBO '):-1]
        print(section)
        func_name = values[event]
        if section == section_names[0]:
            func = shape_dict[func_name]
        elif section == section_names[1]:
            func = func_dict['p'][func_name]
        elif section in section_names[2:4]:
            func = func_dict['s/r'][func_name]
        _VARS['window'].extend_layout(
            _VARS['window'][f'-CHOICES Column {section}-'],\
            param_input_layout(func_name, func)
        )

_VARS['window'].close()