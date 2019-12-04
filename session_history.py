import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import datetime as dt
import os
import random

"""
    Simultaneous PySimpleGUI Window AND a Matplotlib Interactive Window
    A number of people have requested the ability to run a normal PySimpleGUI window that
    launches a MatplotLib window that is interactive with the usual Matplotlib controls.
    It turns out to be a rather simple thing to do.  The secret is to add parameter block=False to plt.show()
"""
sessions = os.listdir("sessions/")

def draw_plot(EAR, timestamp):
   # dates = dts.date2num(timestamp)
   # plt.plot(dates, EAR, xdate=True, ydate=False)
   # plt.show(block=False)
   x = [timestamp[0] + dt.timedelta(seconds=i) for i in range(len(EAR))]
   y = [i + random.gauss(0, 1) for i, _ in enumerate(x)]

   # plot
   plt.plot(x, EAR)
   # beautify the x-labels
   plt.gcf().autofmt_xdate()

   plt.show()

def extract_data(file):
    session = open(r"sessions/"+file[0], 'r')
    EAR_values = []
    timestamps = []
    for line in session:
        for ch in line:
            if ch == "[":
                new_line = session.readline().split(", ")
                try:
                    EAR_values.append(new_line[0][1:])
                    time = dt.datetime.strptime(new_line[1][1:-1], '%H:%M:%S.%f')
                    timestamps.append(time)
                except:
                    print("End of file")
    print(EAR_values)
    print(timestamps)
    draw_plot(EAR_values, timestamps)


sg.change_look_and_feel('DARKBLUE')
layout = [[sg.Button('Plot'), sg.Cancel(), sg.Button('Popup')],
          [sg.Listbox(values=sessions, size=(60, 6), enable_events=True, key='File', default_values=sessions[0])]]

window = sg.Window('Previous Sessions', layout)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Plot':
        draw_plot()
    elif event == 'Popup':
        sg.popup('Yes, your application is still running')
    elif event == 'File':
        extract_data(values['File'])
window.close()