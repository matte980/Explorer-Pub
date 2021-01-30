from tkinter import *
from pathlib import Path
import os

#   INITIALISATION
backgroundColorList = []
folderList = []
sortedFolders = []

lblWidth = 15
canvasPadding = 5
winWidth, winHeight = 700, 600
winX, winY = 300, 200
sorting = 'Alfabetico'
sortOrder = 'Ascendente'
selected = False
currentSelectionCoord = (-1, -1)
currentSelectionName = ''
currentSelection = None
ElementsInRow = 0
capsOrNot = 1
anchorText = 'Anchor SX'
selectedColour = '#cffffd'

fakeEvent = '<KeyPress event keysym=Return keycode=2359309 char=\'\r\' x=-300 y=-228>'

winSettings = str(winWidth) + 'x' + str(winHeight) + '+' + str(winX) + '+' + str(winY)

#   KEY PRESS DICTIONARY for selection moving
passSelectionDict = {
    'Up' : -ElementsInRow,
    'Down' : ElementsInRow,
    'Left' : - 1,
    'Right' : 1
}

#   SORTING MENU
sortingList = [
'Alfabetico',
'Tipo'
] 

textAndImageAnchor = 'nw'

#   PROMBLEMI CON IL RETURN E CON LA PREVDIR

dirName = str(Path.home())
prevDir = dirName

# --------------------------------------------------------

#   CLASS
class container():
    def __init__(self, master, position, row, name):
        global ElementsInRow
        self.master = master
        self.position = position
        self.row = self.position // ElementsInRow
        self.col = self.position % ElementsInRow
        self.name = name
        self.backgroundColor = '#ffffff'
        self.elements()

    def elements(self):
        global imgFile, imgFolder
        global canvasPadding, lblWidth
        global sortedFolders
        global backgroundColorList
        global textAndImageAnchor

        #   FRAME
        self.frame = Frame(self.master, width = 10, height = 50, bg = self.backgroundColor)
        self.frame.grid(row = self.row, column = self.col, sticky = 'nw', padx = canvasPadding)


        #   FILE NAME & IMAGE
        self.fileName = os.path.join(dirName, self.name)
        if os.path.isfile(self.fileName):  
            self.image = Label(self.frame, text=' ', font=('Helvetica', 40), width = 10, height = 40, anchor = textAndImageAnchor, justify = 'left', image = imgFile, compound = CENTER, bg = self.backgroundColor)
        else:
            self.image = Label(self.frame, text=' ', font=('Helvetica', 40), width = 10, height = 40, anchor = textAndImageAnchor, justify = 'left', image = imgFolder, compound = CENTER, bg = self.backgroundColor)

        self.image.grid(row = 0, column = 0, sticky = 'nwe')


        #   LABEL
        self.toWrite = ''
        if len(self.name) > lblWidth:
            nGoBack = len(self.name)//lblWidth
            for i in range(nGoBack+1):
                self.toWrite += self.name[i * lblWidth : (i+1) * lblWidth] + '\n'
        else:
            self.toWrite = self.name

        self.label = Label(self.frame, text=self.toWrite, font=('Helvetica', 10), width = lblWidth, height=2, anchor = textAndImageAnchor, justify = 'left', bg = self.backgroundColor)
        self.label.grid(row = 1, column = 0, sticky = 'nsew')


        # FRAME EVENTS
        self.frame.bind('<Button-1>', self.select)
        self.frame.bind('<Double-1>', self.enter)
        self.frame.bind('<Button-2>', self.rightClick)

        # IMAGE EVENTS
        self.image.bind('<Button-1>', self.select)
        self.image.bind('<Double-1>', self.enter)
        self.image.bind('<Button-2>', self.rightClick)

        # LABEL EVENTS AND GRID
        self.label.bind('<Button-1>', self.select)
        self.label.bind('<Double-1>', self.enter)
        self.label.bind('<Button-2>', self.rightClick)

    def enter(self, event):
        global dirName, prevDir
        gotIn = False
        if os.path.isdir(os.path.join(dirName, self.name)):
            try:
                prevDir = dirName
                dirName = os.path.join(dirName, self.name)
                gotIn = True
                draw()
            except PermissionError:
                print('Accesso non consentito')
                dirName = os.path.dirname(dirName)
                draw()
        return gotIn

    def select(self, event):
        for folder in folderList:
            # if folder.backgroundColor != '#ffffff' and folder != self:
            if folder.backgroundColor != '#ffffff':
                folder.chg_background('#ffffff')
        global dirName
        self.chg_background(selectedColour)
        global currentSelection
        currentSelection = self
        # if self.backgroundColor == '#ffffff':
        #     self.chg_background('#ffff00')
        # else:
        #     self.chg_background('#ffffff')

    def chg_background(self, color):
        self.backgroundColor = color
        self.image.config(bg = color)
        self.label.config(bg = color)

    def move(self, row, col):
        self.row = row
        self.col = col
        global ElementsInRow, canvasPadding
        self.elements()

    def rightClick(self, event):
        print('RIGHT CLICK')
        pass

#   CLASS END
# --------------------------------------------------------
#   FUNCTION START

#   ON EVENT CALL

def keyPressed(event):
    global selected, currentSelection, ElementsInRow, folderList
    # print(event)
    # print(event.keysym)
    if event.keysym == 'BackSpace':
        goBack(fakeEvent)
        currentSelection = None
        return
    elif event.keysym == 'Return' and currentSelection:
        done = currentSelection.enter(fakeEvent)
        if done:
            print('cambiato')
            currentSelection = None
        else: print('STILL HERE')
    if event.keysym in passSelectionDict.keys():
        if currentSelection:
            try:
                folderList[currentSelection.position + passSelectionDict.get(event.keysym)].select(fakeEvent)
            except:
                pass
        elif folderList:
            folderList[0].select(fakeEvent)

def _on_mousewheel(event):
    canvas.yview_scroll(- event.delta, 'units')

def resize(event):
    global winWidth, winHeight, winSettings, ElementsInRow, folderList
    winWidth = root.winfo_width()
    winHeight = root.winfo_height()
    winSettings = str(winWidth) + 'x' + str(winHeight) + '+' + str(winX) + '+' + str(winY)
    temp = getElementsInRow()
    if temp != ElementsInRow:
        ElementsInRow = temp
        for element in folderList:
            element.frame.grid_forget()
            element.image.grid_forget()
            element.label.grid_forget()
        for pos, folder in enumerate(folderList):
            row = pos // ElementsInRow
            col = pos % ElementsInRow
            folder.move(row, col)

def onFrameConfigure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


#   CHANGE VIEW EVENTS

def goBack(event):
    global dirName, canvas, prevDir
    if dirName == os.path.dirname(dirName):
        return
    prevDir = dirName
    dirName = os.path.dirname(dirName)
    # if prevDir != dirName:
    draw()
    canvas.yview_moveto(0)

def previous(event):
    global dirName, canvas, prevDir
    if prevDir != dirName:
        dirName, prevDir = prevDir, dirName
        draw()
        canvas.yview_moveto(0)


#   BUTTON CALLBACKS

def sortCallback(*args):
    global sorting
    if sorting != sortTextVariable.get():
        sorting = sortTextVariable.get()
        draw()

def orderCallback(*args):
    global sortOrder
    if sortOrder != orderTextVariable.get():
        sortOrder = orderTextVariable.get()
        draw()

def anchorChange(event):
    global textAndImageAnchor, anchorText, anchorButton
    anchor = ('nw', 'n')
    textAndImageAnchor = anchor[anchor.index(textAndImageAnchor)-1]
    text = ('Anchor SX', 'Anchor CX')
    anchorText = text[text.index(anchorText)-1]
    anchorButton['text'] = anchorText
    draw()


#   UTILITY FUNCTIONS

def sort(unsortedList):
    global sorting, sortOrder, capsOrNot
    if sorting=='Alfabetico' and sortOrder == 'Ascendente':
        if capsOrNot:
            return sorted(unsortedList)
        else:
            return [x for _,x in sorted(zip([name.lower() for name in unsortedList],unsortedList))]
    elif sorting=='Alfabetico':
        return sorted(unsortedList, reverse = True)
    if sorting == 'Tipo' and sortOrder == 'Ascendente':
        return typeSorting(unsortedList)
    if sorting == 'Tipo':
        return typeSorting(unsortedList)

def typeSorting(unsortedList):
    global sortOrder
    extensions = []
    for element in unsortedList:
        if os.path.isdir(os.path.join(dirName, element)):
            extensions.append('0')
        else:
            extensions.append(element.split('.')[-1])
    if sortOrder == 'Ascendente':
        return [x for _,x in sorted(zip(extensions,unsortedList))]
    return [x for _,x in sorted(zip(extensions,unsortedList), reverse = True)]

def draw():
    global imgFile, imgFolder, folderList
    global canvasPadding, lblWidth
    global backgroundColorList
    for element in folderList:
        element.frame.grid_forget()
        element.image.grid_forget()
        element.label.grid_forget()
    folderList = []
    sortedFolders = sort(os.listdir(dirName))
    root.title(dirName)
    for nCol, folderName in enumerate(sortedFolders):
        nRow = nCol // ElementsInRow
        folderList.append(container(folderFrame, nCol, nRow, folderName))

def getElementsInRow():
    global winWidth, lblWidth, canvasPadding, passSelectionDict
    elInRow = winWidth // int((100*lblWidth/15 + 2 * canvasPadding))
    passSelectionDict['Up'] = - elInRow
    passSelectionDict['Down'] = elInRow
    return elInRow


# ---------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------

#   GUI INTERFACE

#   ROOT
root = Tk()
root.geometry(winSettings)
root.wm_attributes('-topmost', 1)
root.rowconfigure((0,1), weight = 1)
root.columnconfigure(0, weight = 1)
root.bind( '<Configure>', resize)


#   TOP FRAME
topFrame = Frame(root, bg = 'white')
topFrame.pack(expand = 'true', fill = 'both')


#   OPTION FRAME
optionFrame = Frame(topFrame, bg = 'white', height = 20)
optionFrame.pack(fill = 'x')

#   GO BACK BUTTON
goBackButton = Button(optionFrame, text = 'Back')
goBackButton.pack(side = 'left')
goBackButton.bind('<Button-1>', goBack)

#   PREVIOUS BUTTON
previousButton = Button(optionFrame, text = 'Previous')
previousButton.pack(side = 'left')
previousButton.bind('<Button-1>', previous)

#    ANCHOR BUTTON
anchorButton = Button(optionFrame, text = anchorText)
anchorButton.pack(side = 'right')
anchorButton.bind('<Button-1>', anchorChange)


#   SORT ORDER (ASC, DESC) MENU
sortTextVariable = StringVar(optionFrame)
sortTextVariable.set(sortingList[0])

sortingMenu = OptionMenu(optionFrame, sortTextVariable, *sortingList)
sortingMenu.config(width = 10, font=('Helvetica', 12))
sortingMenu.pack(side='left')

sortTextVariable.trace('w', sortCallback)


#   SORT ORDER (ASC, DESC) MENU
sortingOrderList = ['Ascendente', 'Discendente']
orderTextVariable = StringVar(optionFrame)
orderTextVariable.set(sortingOrderList[0])

sortingOrderMenu = OptionMenu(optionFrame, orderTextVariable, *sortingOrderList)
sortingOrderMenu.config(width = 10, font=('Helvetica', 12))
sortingOrderMenu.pack(side='left')

orderTextVariable.trace('w', orderCallback)


#   MAIN CANVAS
canvas = Canvas(topFrame, bg = 'white')
folderFrame = Frame(canvas, bg = 'white')

#   VERTICAL SCROLLBAR
vsb = Scrollbar(topFrame, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side='right', fill='y')

canvas.pack(side='left', fill='both', expand=True)
canvas.create_window((4,4), window=folderFrame, anchor='nw')

folderFrame.bind('<Configure>', onFrameConfigure)

#   EVENTS
topFrame.bind('<Double-1>', goBack)
canvas.bind('<Double-1>', goBack)
folderFrame.bind('<Double-1>', goBack)

#   GLOBAL EVENTS
root.bind_all('<MouseWheel>', _on_mousewheel)
root.bind_all('<Key>', keyPressed)


#   UTILITIES (IMPORT IMAGES AND INITIALIZATION) THAT HAVE TO STAY HERE
imgFile = PhotoImage(file='File.png').subsample(6)
imgFolder = PhotoImage(file='Folder.png').subsample(6)
ElementsInRow = getElementsInRow()


#   DRAW
draw()

#   TKINTER MAINLOOP
root.mainloop()