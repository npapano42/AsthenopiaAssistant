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
sessions = sorted(os.listdir("sessions/"))
plt.rcParams["figure.facecolor"] = "#192734"
plt.rcParams['text.color'] = '#acc2d0'
plt.rcParams['axes.labelcolor'] = '#acc2d0'
plt.rcParams['xtick.color'] = '#acc2d0'
plt.rcParams['ytick.color'] = '#acc2d0'
plt.rcParams['toolbar'] = 'None'

def draw_plot(EAR, timestamp, threshold, canvas):
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
   figure_canvas_agg = FigureCanvasTkAgg(plt.gcf(), canvas)
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


#total session length, and helper function
def sessionlen(timestamps):
  firstTimeStamp = timestamps[0]
  #print(firstTimeStamp)
  lastTimeStamp = timestamps[len(timestamps)-1]
  #print(lastTimeStamp)
  sessionlengthobj = lastTimeStamp-firstTimeStamp
  global length
  length = sessionlengthobj
  return sessionlengthobj

#total session blinks and helper function
def blinksTotal(EAR_values,threshold):
  blinkcounter = 0
  currentlyblinking = False
  for sample in EAR_values:
    if sample<=threshold and not currentlyblinking:
      blinkcounter+=1
      #print("BLINK:",blinkcounter)
      currentlyblinking = True
    if sample>threshold:
      currentlyblinking = False
  global blinks
  blinks = blinkcounter
  return blinkcounter

#average blinks per minute for session
def bpmAVG(EAR_values,timestamps,threshold):
  #print(blinksTotal(EAR_values))
  #print(sessionlen(timestamps).total_seconds())
  avg = round((blinksTotal(EAR_values,threshold)/sessionlen(timestamps).total_seconds())*60, 2)
  global average
  average = avg
  return avg





#TODO
def bpmHigh(EAR_values,timestamps):
  pass

#TODO
def pbmLow(EAR_values,timestamps):
  pass

length = np.nan
blinks = np.nan
average = np.nan

sg.change_look_and_feel('DARKBLUE')

col = [[sg.Listbox(values=sessions, size=(20, 25), enable_events=True, key='File')],
       [sg.Button('Back', key='Back'), sg.Button('Delete', key='Delete')]]

# add the plot to the window
layout =[[sg.Column(col), sg.Canvas(size=(640, 475), key='canvas')],
         [sg.Text('Session Length: ', font=("Helvetica", 25)), sg.Text(str(length), font=("Helvetica", 25), key='length'),
          sg.Text('|  Total Blinks: ', font=("Helvetica", 25)), sg.Text(blinks, font=("Helvetica", 25), key='blinks'),
          sg.Text('|  Blinks/min (avg): ', font=("Helvetica", 25)),  sg.Text(average, font=("Helvetica", 25), key='average')]]
       #  [sg.Text(length, font=("Helvetica", 25)), sg.Text(blinks, font=("Helvetica", 25)), sg.Text(average, font=("Helvetica", 25))]]


window = sg.Window('Session History', layout, element_justification='center', font=("Helvetica", 15), finalize=True).Finalize()

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Back':
        window.close()
    elif event == 'Delete':
        os.remove(r"sessions/"+values['File'][0])
        sessions = os.listdir("sessions/")
        window.FindElement('File').Update(values=sessions)
    elif event == 'File':
        statistics = extract_data(values['File'])
        sessionlength = sessionlen(statistics[1])
        totalsessionBlinks = blinksTotal(statistics[0],statistics[2])
        bpmAverage = bpmAVG(statistics[0],statistics[1],statistics[2])
        print("Session Length: ", sessionlength)
        print("|  Blinks in this session: ",totalsessionBlinks)
        print("|  Average Blinks Per Minute: ",bpmAverage)
        window.FindElement('length').Update(str(int(length.seconds//60))+ ":" + str(int(length.seconds%60)))
        window.FindElement('blinks').Update(blinks)
        window.FindElement('average').Update(average)
        print(average)
        fig_canvas_agg = draw_plot(statistics[0], statistics[1], statistics[2], window['canvas'].TKCanvas)


window.close()
