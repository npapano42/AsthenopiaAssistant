import PySimpleGUI as sg
import matplotlib.pyplot as plt
import datetime as dt
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
    Simultaneous PySimpleGUI Window AND a Matplotlib Interactive Window
    A number of people have requested the ability to run a normal PySimpleGUI window that
    launches a MatplotLib window that is interactive with the usual Matplotlib controls.
    It turns out to be a rather simple thing to do.  The secret is to add parameter block=False to plt.show()
"""
sessions = os.listdir("sessions/")
plt.rcParams["figure.facecolor"] = "#192734"
plt.rcParams['text.color'] = '#acc2d0'
plt.rcParams['axes.labelcolor'] = '#acc2d0'
plt.rcParams['xtick.color'] = '#acc2d0'
plt.rcParams['ytick.color'] = '#acc2d0'
plt.rcParams['toolbar'] = 'None'

def draw_plot(EAR, timestamp, threshold):
   # plot
   plt.clf()
   plt.plot(timestamp, EAR, color='w')
   plt.axhline(y=threshold, color='0.5', linestyle='--')
   # beautify the plot
   ax = plt.gca()
   ax.set_facecolor('#325266')
   plt.gcf().autofmt_xdate()
   ax.set_xlabel('Time')
   ax.set_ylabel('Eye Aspect Ratio (EAR)')
   plt.title('Session from ' + timestamp[0].strftime("%H:%M:%S") + ' to ' + timestamp[(len(timestamp) - 1)].strftime("%H:%M:%S"))
   #plt.ylabel('Eye Aspect Ratio (EAR)', color='#acc2d0')
   #plt.xlabel('Time', color='#acc2d0')
   return plt.gcf()
   figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.close_event()
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def extract_data(file):
    session = open(r"sessions/"+file[0], 'r')
    EAR_values = []
    timestamps = []
    session.readline()
    threshold = float(session.readline())
    for line in session:
        for ch in line:
            if ch == "[":
                new_line = session.readline().split(", ")
                try:
                    EAR_values.append(float(new_line[0][1:]))
                    time = dt.datetime.strptime(new_line[1][1:-1], '%H:%M:%S.%f')
                    timestamps.append(time)
                except:
                    print("End of file")
    print(timestamps)
    print(threshold)
    print(EAR_values)
    EAR_values = [np.nan if value == -1.0 else value for value in EAR_values]
    print(EAR_values)
    return[EAR_values, timestamps, threshold]


sg.change_look_and_feel('DARKBLUE')
layout = [[sg.Canvas(size=(640, 475), key='canvas')],
          [sg.Listbox(values=sessions, size=(60, 6), enable_events=True, key='File')]]

# add the plot to the window


window = sg.Window('Session History', layout, element_justification='center', font=("Helvetica", 15), finalize=True)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'File':
        graph_helper = extract_data(values['File'])
        fig_canvas_agg = draw_figure(window['canvas'].TKCanvas, draw_plot(graph_helper[0], graph_helper[1], graph_helper[2]))


window.close()