import PySimpleGUI as sg
import blink_detection


times = [15, 30, 60, 'Indefinite']

### Set window layout
sg.change_look_and_feel('DARKBLUE')
layout = [  [sg.Text('For how long should Asthenopia Assistant track your blinks?')],
            [sg.Combo([str(times[0]) + ' minutes', str(times[1]) + ' minutes', str(times[2]) + ' minutes', times[3]], enable_events=True, key='combo', default_value=times[3])],
            [sg.Button('Start',  key='start')],
            [sg.Button('Past Sessions', key='History')]]

### Create the Window
window = sg.Window('Asthenopia Assistant', layout, element_justification='center', font=("Helvetica", 15), finalize=True)

first_run = True
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event is None:
        break
    if event in ('start'):   # if user closes window or clicks cancel
        try:
            print(int(values['combo'][:2]))
        except:
            print(-1)
        blink_detection.start_program()
        break
    elif event in ('History'):
        if first_run:
            import session_history
            first_run = False
        else:
            import importlib
            importlib.reload(session_history)
window.close()

