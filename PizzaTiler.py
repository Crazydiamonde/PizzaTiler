import os
import PIL
from PIL import Image, ImageTk
import sys
import tkinter as tk
from tkinter import filedialog

#Tiles are 36x36... I think

sizeThing = 36

thing2 = 10

class Vector2:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    def get(self):
        return (self.x, self.y)

def folders(pizzadir):
    if not os.path.isdir(pizzadir):
        os.makedirs(pizzadir)
    if not os.path.isdir(pizzadir + "/Tilesets"):
        os.makedirs(pizzadir + "/Tilesets")
    if not os.path.isdir(pizzadir + "/Tilemaps"):
        os.makedirs(pizzadir + "/Tilemaps")      

def setup(windowSize):
    root = tk.Tk()
    
    window = tk.Toplevel(root)
    root.withdraw()
    window.resizable(False, False)
    window.title("Pizza Tiler by Crazine")
    window.geometry(str(windowSize.x) + "x" + str(windowSize.y))
    window.configure(bg = '#b0b0b0')
    
    pizzadir = os.environ['USERPROFILE'] + "/PizzaTiler"
    folders(pizzadir)
    return root, window, pizzadir

def makeIntoTiles(image):
    tiles = []
    gridSizeX = int(image.size[0] / sizeThing)
    gridSizeY = int(image.size[1] / sizeThing)
    for j in range(gridSizeY):
        for i in range(gridSizeX):
            tiles.append(image.crop((i * sizeThing, j * sizeThing, (i + 1) * sizeThing, (j + 1) * sizeThing)))
    return tiles
    
def keyReader(key):
    if key.char == "i":
        importTileset(pizzadir)
    if key.char == "o":
        tileset = filedialog.askdirectory(initialdir = pizzadir + "/Tilesets")  
        renderEverything(h.canvas, pizzadir, h.level, tileset)
    if key.char == "s":
        saveLevel(h.level)
    
class holder:
    def __init__ (self):
        self.e = 0
    
def saveLevel(level, name):
    export = ""
    with open(name, 'w') as levelsave:
        for row in level:
            word = ""
            for pos, thing in enumerate(row):
                word += str(thing)
                if pos != len(row) - 1:
                    word += ";"
            export += word[:] + "\n"
        levelsave.write(export)
    
def importTileset(pizzadir):
    fileset = filedialog.askopenfilename()
    if not fileset:
        return
    name = pizzadir + "/Tilesets/" + os.path.basename(fileset)[:len(os.path.basename(fileset)) - 4]
    tileset = Image.open(fileset)
    tiles = makeIntoTiles(tileset)
    for pos, t in enumerate(tiles):
        if not os.path.isdir(name):
            os.makedirs(name)
        t.save(name + "/" + str(pos) + ".png")  

def loadTiles(pizzadir, name):
    size = len(os.listdir(pizzadir + "/Tilesets/" + name))
    name2 = pizzadir + "/Tilesets/" + name + "/"
    things = []
    for i in range(size):
        image1 = Image.open(name2 + str(i) + ".png")
        image2 = ImageTk.PhotoImage(image1)
        things.append(image2)
    return things

def renderEverything(window, pizzadir, level, tileset):
    h.tileSave = []
    window.delete("all")
    tiles = loadTiles(pizzadir, os.path.basename(tileset))
    for i, t in enumerate(tiles):
        h.tileSave.append(t)
        x = i % thing2
        y = int(i / thing2)
        window.create_image(x * sizeThing, y * sizeThing, anchor=tk.NW, image = t)
    window.create_line(thing2 * sizeThing, 0, thing2 * sizeThing, 1080-120, width=2)
    window.create_line(0, 1080-120, 1920, 1080-120, width=2)
    
    #level
    for y, row in enumerate(level):
        for x, thing in enumerate(row):
            window.create_image(x * sizeThing + thing2 * sizeThing, y * sizeThing, anchor=tk.NW, image = h.tileSave[thing])
    
    if os.path.isfile(tileset + "/" + str(h.selected) + ".png"):
        x = h.selected % thing2
        y = int(h.selected / thing2)
        
        window.create_rectangle(x * sizeThing, y * sizeThing, (x + 1) * sizeThing, (y + 1) * sizeThing, outline="red")
    
    for pos, button in enumerate(h.b):
        button.place(x=pos*384, y=1080-120, width=384, height=120)
    
    return window

def renderUpdate(tileX, tileY, window, pizzadir, level, tileset):  
    
    window.create_rectangle((tileX + thing2) * sizeThing - 1, tileY * sizeThing - 1, (tileX + thing2 + 1) * sizeThing + 2, (tileY + 1) * sizeThing + 2, fill="#f0f0f0", outline="#f0f0f0")
    
    for y, row in enumerate(level):
        if y > tileY - 2 and y < tileY + 2:
            for x, thing in enumerate(row):
                if x > tileX - 2 and x < tileX + 2:
                    window.create_image(x * sizeThing + thing2 * sizeThing, y * sizeThing, anchor=tk.NW, image = h.tileSave[thing])
    for pos, button in enumerate(h.b):
        button.place(x=pos*384, y=1080-120, width=384, height=120)    
    

def clickReader(event):
    x = event.x
    y = event.y
    if y < 1080 - 120:
        if x < thing2 * sizeThing: #in tiles
            tileX = int(x / sizeThing)
            tileY = int(y / sizeThing)
            h.selected = tileX + tileY * thing2
            renderEverything(h.canvas, pizzadir, h.level, h.tileset)
        else:
            tileX = int((x - thing2 * sizeThing) / sizeThing)
            tileY = int(y / sizeThing)
            h.level[tileY][tileX] = h.selected
            renderUpdate(tileX, tileY, h.canvas, pizzadir, h.level, h.tileset)

def dragReader(event):
    x = event.x
    y = event.y
    if x > thing2 * sizeThing and y < 1080 - 120:
        tileX = int((x - thing2 * sizeThing) / sizeThing)
        tileY = int(y / sizeThing)
        h.level[tileY][tileX] = h.selected
        renderUpdate(tileX, tileY, h.canvas, pizzadir, h.level, h.tileset)

def middleClickReader(event):
    x = event.x
    y = event.y    
    tileX = int((x - thing2 * sizeThing) / sizeThing)
    tileY = int(y / sizeThing)
    h.selected = h.level[tileY][tileX]
    renderEverything(h.canvas, pizzadir, h.level, h.tileset)  

def unpackcsv(file):
    unpacked = [[]]
    i = 0
    word = ""
    for char in file:
        if char == "\n":
            unpacked[i].append(int(word))
            word = ""
            i += 1
            unpacked.append([])
        elif char == ";":
            unpacked[i].append(int(word))
            word = ""
        else:
            word += char
    return unpacked

def done(x, y, window2):
    h.level = [[0 for i in range(x)] for i2 in range(y)]
    renderEverything(h.canvas, pizzadir, h.level, h.tileset)
    window2.destroy()

def newlevel():
    window2 = tk.Toplevel(root)
    window2.title("New Level")
    window2.geometry("800x600")
    canvas2 = tk.Canvas(window2, width=200, height=200)
    canvas2.pack()
    canvas2.place(x=0, y=0)
    width = tk.Text(canvas2, width = 40, height = 2)
    width.place(x=0, y=0)
    height = tk.Text(canvas2, width = 40, height = 2)
    height.place(x=0, y=40)    
    doneB = tk.Button(canvas2, text = "Done", command = lambda:done(int(width.get("1.0", tk.END)), int(height.get("1.0", tk.END)), window2))
    doneB.config(font = ("Helvetica", 20))   
    doneB.place(x=0, y=80)

def openlevel():
    levelToOpen = filedialog.askopenfilename(initialdir = pizzadir + "/Tilemaps")
    with open(levelToOpen, "r") as file:
        unpacked = unpackcsv(file.read())
    h.level = unpacked
    renderEverything(h.canvas, pizzadir, h.level, h.tileset)

def savelevel():
    destination = filedialog.asksaveasfilename(filetypes = [(("Tile Map", "*.csv"))], initialdir = pizzadir + "/Tilemaps")
    saveLevel(h.level, destination)

def importtiles():
    importTileset(pizzadir)

def opentiles():
    tileset = filedialog.askdirectory(initialdir = pizzadir + "/Tilesets")
    h.tileset = tileset
    renderEverything(h.canvas, pizzadir, h.level, h.tileset)

def buttons():
    buttons = []
    button1 = tk.Button(window, command = newlevel, text = "New Level")
    button1.place(x=0, y=1080 - 120)
    button1.config(font = ("Helvetica", 50))    
    buttons.append(button1)
    
    button2 = tk.Button(window, command = openlevel, text = "Open Level")
    button2.place(x=0, y=1080 - 120)
    button2.config(font = ("Helvetica", 50))    
    buttons.append(button2)
    
    button3 = tk.Button(window, command = savelevel, text = "Save Level")
    button3.place(x=0, y=1080 - 120)
    button3.config(font = ("Helvetica", 50))    
    buttons.append(button3)
    
    button4 = tk.Button(window, command = importtiles, text = "Import Tiles")
    button4.place(x=0, y=1080 - 120)
    button4.config(font = ("Helvetica", 50))    
    buttons.append(button4)
    
    button5 = tk.Button(window, command = opentiles, text = "Open Tiles")
    button5.place(x=0, y=1080 - 120)
    button5.config(font = ("Helvetica", 50))    
    buttons.append(button5)    
    return buttons

def loop(root, window, pizzadir, h, buttonS):
    
    window.bind("<KeyPress>", keyReader)
    window.bind("<Button-1>", clickReader)
    window.bind("<B1-Motion>", dragReader)
    window.bind("<Button-2>", middleClickReader)
    
    level = [[0 for i in range(10)] for i in range(10)]
    
    canvas = tk.Canvas(window, width = screenSize.x, height = screenSize.y - 120)
    canvas.pack()
    images = []
    
    
    tileset = pizzadir + "/Tilesets/collision"
    
    h.canvas = canvas
    h.level = level
    h.selected = False
    h.tileset = tileset
    h.tileSave = []    
    h.b = buttonS
    
    renderEverything(canvas, pizzadir, level, tileset)
    
    
    root.mainloop()

h = holder()
screenSize = Vector2(1920, 1080) 
root, window, pizzadir = setup(screenSize)
buttonS = buttons()
tileset = False
loop(root, window, pizzadir, h, buttonS)