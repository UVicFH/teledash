import json
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

# stolen from https://towardsdatascience.com/how-to-flatten-deeply-nested-json-objects-in-non-recursive-elegant-python-55f96533103d
def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def runProcess ():
    # open file
    file = open(openFile, "r")

    # read header lines
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()

    # start first data point
    line = file.readline()
    data = json.loads(str(line).replace("'", ""))
    # print(line)

    line = file.readline()
    totalLines = 0
    while line:
        # read successive data points
        data2 = json.loads(str(line).replace("'", ""))
        data.update(data2)
        line = file.readline()
        totalLines = totalLines + 1

    # flatten data
    flatdata = flatten_json(data)

    # form a data template
    template = {}
    for key in flatdata:
        item = '{"' + str(key) + '": 0}'
        z = json.loads(item)
        template.update(z)


    # print the data template
    print("Data template:")
    print(json.dumps(template, indent = 4))
    print("Total lines in file: " + str(totalLines))

    # open a csv file to write output to
    output = open(outputFile,"w+")
    for key in template:
        output.write(str(key) + ",")
    output.write("\n")

    # go back to top of file
    file.seek(0)

    # read header lines
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()

    # start first data point
    line = file.readline()
    linesProcessed = 0
    printed = 0
    while line:
        # read successive data points
        data2 = json.loads(str(line).replace("'", ""))
        # save to storage template
        template.update(flatten_json(data2))
        # add current data structure to the csv
        for element in template:
            output.write(str(template[element]) + ",")
        output.write("\n")
        # get next line
        line = file.readline()
        linesProcessed = linesProcessed + 1
        if(round(linesProcessed * 100 / totalLines) % 5 == 0):
            if(printed == 0):
                progress['value'] = round(linesProcessed * 100 / totalLines)
                window.update_idletasks()
                print("Progress: " + str(round(linesProcessed * 100 / totalLines)) + "%")
                printed = 1
        else:
            printed = 0
                  
    # close file
    file.close()
    output.close()

def openFile ():
    global openFile
    openFile = filedialog.askopenfilename(title = "Select Datalog File",filetypes = (("text files","*.txt"),("all files","*.*")))

def saveLocation ():
    global outputFile
    outputFile = filedialog.asksaveasfilename(title = "Select Save Location",filetypes = (("csv file","*.csv"),("all files","*.*")))

# start a window
window = tkinter.Tk()
window.title("UVic Hybrid Telemetry Decoder")

canvas1 = tkinter.Canvas(window, width = 600, height = 360, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

label1 = tkinter.Label(window, text='UVic Hybrid Telemetry Decoder', bg = 'lightsteelblue2')
label1.config(font=('helvetica', 20))
canvas1.create_window(300, 60, window=label1)

openFileButton = tkinter.Button(text="Import Recorded Data", command=openFile, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 120, window=openFileButton)

saveFileButton = tkinter.Button(text="Select Save Location", command=saveLocation, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 180, window=saveFileButton)

runButton = tkinter.Button(text="Run", command=runProcess, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 240, window=runButton)

# declare progress bar now so can be modified in functions
progress = Progressbar(window,orient=HORIZONTAL,length=300,mode='determinate')
canvas1.create_window(300, 300, window=progress)

window.mainloop()
