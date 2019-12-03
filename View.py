from tkinter import *
from tkinter.ttk import Combobox
import blink_detection

### Create window object
root = Tk()
root.title('Asthenopia Assistant')
root.geometry('750x350')


# Title
part_text = StringVar()
part_label = Label(root, text='Asthenopia Assistant', font=('bold', 30), pady=20)
part_label.pack(side='top')

# Start Label
part_text = StringVar()
part_label = Label(root, text='Select Time Interval', font=('bold', 20), pady=20)
part_label.pack(side='top')

#Dropdown options
time = StringVar()
time_Options = ['15 minutes', '30 minutes', '60 minutes', 'Indefinte']
combo = Combobox(root, values =time_Options)
combo.pack(side = 'top')

#Defining Start function
def startProgram():
    root.withdraw() #Hide homescreen
    print(combo.get())
    b= blink_detection.start_program() # call blink detection

#Start Button
start_Button = Button(root, text ='Start', command = startProgram)
start_Button.pack(side='top')

#Start program
root.mainloop()