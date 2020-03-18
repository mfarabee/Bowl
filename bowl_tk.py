# Written by Mike Farabee 2/24/2020
VERSION=0.5
import sys
import math
import struct
import os.path
try:
    from Tkinter import *
except:
    from tkinter import *

try:
    import tkFileDialog
    import tkMessageBox
except:
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox

try:
    import ttk
except:
    from tkinter import ttk


InputData={
    'units':'in',
    'diameter':3.0,
    'depth':0.5,
    'zSafety':0.50,
    'roughCut':0.25,
    'finishCut':0.1,
    'roughStep':100,
    'finishStep':5,
    'feed':100,
    'spindleSpeed':6000,
    'cutterDiameter':0.5,
    'enableCoolant':1,
    'outfile':"bowl.gcode",
    'outdir':"."
}


#units="mm"
#depth=19.05
#zSafety=5.0
#roughCut=6.35
#finishCut=2.54
#diameter=76.2

lineNum=100
lineInc=5

def convert():
    global InputData
    if InputData['units'].get() == 'in':
        InputData['feed'].set(round(float(InputData['feed'].get())/25.4,5))
        InputData['diameter'].set(round(float(InputData['diameter'].get())/25.4,5))
        InputData['depth'].set(round(float(InputData['depth'].get())/25.4,5))
        InputData['zSafety'].set(round(float(InputData['zSafety'].get())/25.4,5))
        InputData['roughCut'].set(round(float(InputData['roughCut'].get())/25.4,5))
        InputData['finishCut'].set(round(float(InputData['finishCut'].get())/25.4,5))
        InputData['cutterDiameter'].set(round(float(InputData['cutterDiameter'].get())/25.4,5))
    else:
        InputData['feed'].set(round(float(InputData['feed'].get())*25.4,5))
        InputData['diameter'].set(round(float(InputData['diameter'].get())*25.4,5))
        InputData['depth'].set(round(float(InputData['depth'].get())*25.4,5))
        InputData['zSafety'].set(round(float(InputData['zSafety'].get())*25.4,5))
        InputData['roughCut'].set(round(float(InputData['roughCut'].get())*25.4,5))
        InputData['finishCut'].set(round(float(InputData['finishCut'].get())*25.4,5))
        InputData['cutterDiameter'].set(round(float(InputData['cutterDiameter'].get())*25.4,5))

def openFileForSave(valueHash):
        tmp=tkFileDialog.asksaveasfilename(title='browse',defaultextension='gcode',initialdir=valueHash["outdir"])
        if tmp != None:
            valueHash["outfile"].set(tmp)

def openDirectory(valueHash):
        tmp=tkFileDialog.askdirectory(title='browse')
        if tmp != None:
            valueHash["outdir"].set(tmp)

def Starting(units, diameter, depth, zSafety, roughCut, finishCut, feed,
    spindleSpeed, cutterDiameter, enableCoolant, outfile):
    global lineInc
    global lineNum
    global VERSION

    print("(Bowl Cutter By Mike Farabee Version:%3.1f)"%(VERSION))
    print("(Units:%s Diameter:%5.4f Depth:%5.4f Rough:%5.4f Finish:%5.4f)"%(units,diameter,depth,roughCut,finishCut))
    print("(Spindle:%d Feed:%d Cutter Diameter:%5.4f)"%(spindleSpeed,feed,cutterDiameter))
    if units == "in":
        print("N%d G20 (Inch)"%(lineNum))
    else:
        print("N%d G21 (metric)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G17 (XY Plane)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G90 (Absolute)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G40 (Cancel Cutter Compansation)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G49 (Cancel Tool Offset)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G80 (Cancel Fixed Cycle)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G94 (Feedrate Units per min)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d M06 T1 (Tool Change)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d M03 S%d (Spindle on CW, Speed)"%(lineNum,spindleSpeed))
    lineNum=lineNum+lineInc
    if enableCoolant==1:
        print("N%d M08 (Coolant On)"%(lineNum))
        lineNum=lineNum+lineInc
    print("N%d G18 (ZX plane)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G0 Z%5.4f F%5.2f (Set Feed Rate and Inital Height)"%(lineNum,depth+zSafety,feed))
    lineNum=lineNum+lineInc
    print("")
    lineNum=lineNum+lineInc

def Ending(enableCoolant):
    global lineInc
    global lineNum
    lineNum=int((lineNum+100)/100)*100
    print("N%d M5 (Spindle Stop)"%(lineNum))
    lineNum=lineNum+lineInc
    print("N%d G17 (XY plane)"%(lineNum))
    lineNum=lineNum+lineInc
    if enableCoolant==1:
        print("N%d M09 (Coolant Off)"%(lineNum))
        lineNum=lineNum+lineInc
    print("N%d M30 (Program End)"%(lineNum))
    lineNum=lineNum+lineInc


def createLabelEntry(parentFrame,labelName,varHash,varKey,varDefault):

    if type(varDefault) != type("") and type(varDefault) != type(1) and type(varDefault) != type(1.0):
        defaultValue=varDefault.get()
    else:
        defaultValue=varDefault

    if type(varHash[varKey]) == type("") or type(varHash[varKey]) == type(1) or type(varHash[varKey]) == type(1.0):
        varHash[varKey]=StringVar()
        varHash[varKey].set(defaultValue)

    entryFrame=Frame(parentFrame)
    entryFrame.pack(side="top",expand=True,fill="x")
    entryLabel=Label(entryFrame,text=labelName,justify="left")
    entryLabel.pack(side="left")
    entryBox=Entry(entryFrame,textvariable=varHash[varKey],justify='right').pack(side="left",expand=True,fill="x")
    return(entryFrame)


def createGcode(units, diameter, depth, zSafety, roughCut, finishCut, roughStep, finishStep,
    feed,spindleSpeed, cutterDiameter, enableCoolant, outfile):
    global lineInc
    global lineNum
    cuts=[]
    lineNum=100
    originalStdout=""

    if outfile != "":
        originalStdout = sys.stdout
        sys.stdout = open(outfile,"w")

    diameter=float(diameter)
    depth=float(depth)
    zSafety=float(zSafety)
    roughCut=float(roughCut)
    finishCut=float(finishCut)
    feed=float(feed)
    spindleSpeed=int(spindleSpeed)
    cutterDiameter=float(cutterDiameter)
    enableCoolant=int(enableCoolant)
    roughStep=cutterDiameter*(float(roughStep)/100)
    finishStep=cutterDiameter*(float(finishStep)/100)

    compensatedDiameter=diameter-(cutterDiameter/2)
    radius=(((compensatedDiameter*compensatedDiameter)/(8*depth))+(depth/2))
    #radiusOffset= radius-depth

    #Create Cut Depth List
    result=depth-roughCut
    while result>finishCut:
        cuts.append(depth-result)
        result=result-roughCut
    result=result+roughCut
    if result >finishCut:
        cuts.append(depth-finishCut)
    cuts.append(depth)

    Starting(units, diameter, depth, zSafety, roughCut, finishCut, feed,
        spindleSpeed, cutterDiameter, enableCoolant, outfile)

    for incDepth in (cuts):
        lineNum=int((lineNum+100)/100)*100
        # C= sqrt( (8*D*R) - (d*d*4) )
        #Calculate incremental diameter based onincremental depth
        incDia=math.sqrt((8*incDepth*radius) - (incDepth*incDepth*4))
        halfDia=incDia/2.0
        radiusOffset=radius-incDepth
        if (depth-incDepth)<0.001:
            stepSize=finishStep
        else:
            stepSize=roughStep


        # Start at top, calculate the width and step
        #for a in range(89,-90,segments):
            #aR=math.radians(a)
        y=halfDia-stepSize
        x=math.sqrt((halfDia*halfDia)-(y*y))
        print("(Depth=%5.4f  Diameter: %5.4f  Step:%5.4f)"%(incDepth,incDia+(cutterDiameter/2.0),stepSize))
        print("N%d G0 X-%5.4f Y%5.4f Z%5.4f"%(lineNum,x,y,zSafety))
        lineNum=lineNum+lineInc
        inc=0
        prevX=0
        prevY=0
        while y > -(halfDia-0.00001): #subtract 0.00001 to avoid floating point accuracy issues
            #x=math.cos(aR)*(incDia/2.0)
            #y=math.sin(aR)*(incDia/2.0)

            if inc==0:
                if prevX==0 and prevY==0: #First time
                    print("N%d G1 X%5.4f Y%5.4f Z0.0"%(lineNum,-x,y))
                else:
                    print("N%d G17 G3 X%5.4f Y%5.4f I%5.4f  J%5.4f"%(lineNum,-x,y,prevX,-prevY))
                lineNum=lineNum+lineInc
                print("N%d G18 G2 X%5.4f Y%5.4f I%5.4f K%5.4f"%(lineNum,x,y,x,radiusOffset))
                inc=1
            else:
                #print("N%d G1 X%5.4f Y%5.4f Z0.0"%(lineNum,x,y))
                print("N%d G17 G2 X%5.4f Y%5.4f I%5.4f J%5.4f"%(lineNum,x,y,-prevX,-prevY))
                lineNum=lineNum+lineInc
                print("N%d G18 G3 X%5.4f Y%5.4f I%5.4f K%5.4f"%(lineNum,x*-1,y,x*-1,radiusOffset))
                inc=0
            lineNum=lineNum+lineInc
            prevX=x
            prevY=y
            y=y-stepSize
            x=math.sqrt(abs((halfDia*halfDia)-(y*y)))

        print("N%d G0 Z%5.4f"%(lineNum,zSafety))
        lineNum=lineNum+lineInc
    lineNum=int((lineNum+100)/100)*100
    Ending(enableCoolant)

    # Close the output file and reset sdtout, if it was redirected
    if originalStdout != "":
        sys.stdout.close
        sys.stdout = originalStdout

    tkMessageBox.showinfo("Information","Gcode Saved!")

#############
#    MAIN
#############


frame={}
top=Tk()
frame["main"]=Frame(top)
frame["main"].pack(side="top",fill="x",anchor="ne")
frame["menubar"]=Frame(frame["main"])
frame["menubar"].pack(side="top",fill="x",anchor="ne")
frame["body"]=Frame(frame["main"])
frame["body"].pack(side="top",fill="x",anchor="ne")

#InputDat={}
tmp=InputData["enableCoolant"]
InputData["enableCoolant"]=StringVar()
InputData["enableCoolant"].set(tmp)
tmp=InputData["outfile"]
InputData['outfile']=StringVar()
InputData['outfile'].set(tmp)
tmp=InputData["units"]
InputData["units"]=StringVar()
InputData["units"].set(tmp)

# pulldown
menubar=Menu(frame["menubar"])
#filemenu=Menu(menubar)
#filemenu.add_command(label="Save Config",command=lambda: saveConfig(InputData))
#filemenu.add_command(label="Quit",command=lambda: top.destroy())
#menubar.add_cascade(label="File",menu=filemenu)

#helpmenu=Menu(menubar)
#helpmenu.add_command(label="Help",command=lambda: displayText("Help",HELPSTRING))
#helpmenu.add_command(label="About",command=lambda: displayText("About",ABOUTSTRING))
#menubar.add_cascade(label="Help",menu=helpmenu)


frame["Machine"]=LabelFrame(frame["body"],bd=2,text="Machine")
frame["Machine"].pack(side="top",fill="x",anchor="ne")
frame["units"]=Frame(frame["Machine"])

frame["units"].pack(side="top",expand=True,fill="x")
Label(frame["units"],text="Dimension Units").pack(side="left")
Radiobutton(frame["units"],text="mm",padx=20,variable=InputData["units"],value="mm",command=convert).pack(side="left")
Radiobutton(frame["units"],text="inch",padx=20,variable=InputData["units"],value="in",command=convert).pack(side="left")

frame["coolant"]=Frame(frame["Machine"])
frame["coolant"].pack(side="top",expand=True,fill="x")
Label(frame["coolant"],text="Coolant").pack(side="left")
Radiobutton(frame["coolant"],text="Disable",padx=20,variable=InputData["enableCoolant"],value=0).pack(side="left")
Radiobutton(frame["coolant"],text="Enable",padx=20,variable=InputData["enableCoolant"],value=1).pack(side="left")

frame["zSafety"]=createLabelEntry(frame["Machine"],"Z Safety",
        InputData,"zSafety",InputData["zSafety"])
Label(frame["zSafety"],textvariable=InputData['units']).pack(side="left")

frame["Spindle"]=createLabelEntry(frame["Machine"],"Spindle Speed",
        InputData,"spindleSpeed",InputData["spindleSpeed"])
Label(frame["Spindle"],text="rpm").pack(side="left")

frame["Feed"]=createLabelEntry(frame["Machine"],"Feed Rate",
        InputData,"feed",InputData["feed"])
Label(frame["Feed"],textvariable=InputData['units']).pack(side="left")
Label(frame["Feed"],text="/min").pack(side="left")

frame["bowl"]=LabelFrame(frame["body"],bd=2,text="Bowl Dimensions")
frame["bowl"].pack(side="top",fill="x",anchor="ne")
frame["bowlDia"]=createLabelEntry(frame["bowl"],"Diameter",
        InputData,"diameter",InputData["diameter"])
Label(frame["bowlDia"],textvariable=InputData['units']).pack(side="left")
frame["depth"]=createLabelEntry(frame["bowl"],"Depth",InputData,"depth",InputData["depth"])
Label(frame["depth"],textvariable=InputData['units']).pack(side="left")

frame["Tool"]=LabelFrame(frame["body"],bd=2,text="Tool")
frame["Tool"].pack(side="top",fill="x",anchor="ne")
frame["ToolDiameter"]=createLabelEntry(frame["Tool"],"Diameter",
        InputData,"cutterDiameter",InputData["cutterDiameter"])
Label(frame["ToolDiameter"],textvariable=InputData['units']).pack(side="left")

frame["Rough"]=createLabelEntry(frame["Tool"],"Rough Cut",
        InputData,"roughCut",InputData["roughCut"])
Label(frame["Rough"],textvariable=InputData['units']).pack(side="left")

frame["Finish"]=createLabelEntry(frame["Tool"],"Finish Cut",
        InputData,"finishCut",InputData["finishCut"])
Label(frame["Finish"],textvariable=InputData['units']).pack(side="left")

frame["RoughStep"]=createLabelEntry(frame["Tool"],"Rough Step",
        InputData,"roughStep",InputData["roughStep"])
Label(frame["RoughStep"],text="%").pack(side="left")

frame["FinishStep"]=createLabelEntry(frame["Tool"],"Finish Step",
        InputData,"finishStep",InputData["finishStep"])
Label(frame["FinishStep"],text="%").pack(side="left")

frame["output"]=LabelFrame(frame["body"],bd=2,text="Output Gcode")
frame["output"].pack(side="top",fill="x",anchor="ne")
frame["outApply"]=createLabelEntry(frame["output"],"Save As",InputData,
        "outfile",InputData["outfile"])
fileButton=Button(frame["outApply"],text="^",
        command= lambda: openFileForSave(InputData)).pack(side="right")

buttonFrame2=Frame(frame["body"])
buttonFrame2.pack(side="bottom",fill="x",anchor="s")
applyButton2=Button(buttonFrame2,
    text="Apply",
    command= lambda: createGcode(
        InputData['units'].get(),
        InputData['diameter'].get(),
        InputData['depth'].get(),
        InputData['zSafety'].get(),
        InputData['roughCut'].get(),
        InputData['finishCut'].get(),
        InputData['roughStep'].get(),
        InputData['finishStep'].get(),
        InputData['feed'].get(),
        InputData['spindleSpeed'].get(),
        InputData['cutterDiameter'].get(),
        InputData['enableCoolant'].get(),
        InputData['outfile'].get()))
applyButton2.pack(side="right")


top.config(menu=menubar)



top,mainloop()
