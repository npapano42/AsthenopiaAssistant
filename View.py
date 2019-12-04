import PySimpleGUI as sg
import blink_detection

times = [15, 30, 60, 'Indefinite']

### Set window layout
sg.change_look_and_feel('DARKBLUE')
layout = [  [sg.Text('How long should Asthenopia Assistant track your blinks?')],
            [sg.Combo([str(times[0]) + ' minutes', str(times[1]) + ' minutes', str(times[2]) + ' minutes', times[3]], enable_events=True, key='combo')],
            [sg.Button('Start',  key='start')]]

### Create the Window
window = sg.Window('Asthenopia Assistant', layout, element_justification='center', font=("Helvetica", 15))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in ('start'):   # if user closes window or clicks cancel
        try:
            print(int(values['combo'][:2]))
        except:
            print(-1)
        blink_detection.start_program()
        break
    if event is None:
        break
window.close()

