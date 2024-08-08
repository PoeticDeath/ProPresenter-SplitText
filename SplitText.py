import os
import wx
import json
import tkinter as tk
import urllib.request
from time import sleep

app = []; app = wx.App(None)
dc = wx.ScreenDC()
x = 3840
y = 2160
screens = 3
maxsize = size = 250
myFont = wx.Font(size, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True)
dc.SetFont(myFont)

if os.name != "nt":
    root = tk.Tk()
    root.geometry(f"{x}x{y}+5760+0")
    root.config(bg = "#add")
    root.wm_attributes("-transparentcolor", "#add")
    root.overrideredirect(1)

    T = []
    for i in range(screens):
        T += [tk.Text(root)]
        T[i].config(bg = "#add", fg = "white", font = ("Arial", size), borderwidth = 0, wrap = "none")
        T[i].pack()
        T[i].place(x = (x // screens) * i, y = 0, width = x // screens, height = y)
        Just = "center"
        if i == 0:
            Just = "right"
        if i == screens - 1:
            Just = "left"
        T[i].tag_config("Just", justify = Just)

def main(string):
    strings = [[" "] for i in range(screens)]
    splitstring = string.split(" ")
    o = 0
    added = 0
    maxadd = 0
    for i in splitstring:
        if ((dc.GetTextExtent(strings[o][-1] + " " + i + " ").x > (x // screens) and added > 10) or (strings[o][-1].count(" ") > 2)) and strings[o][-1][-1] != "'":
            strings[o] += [" "]
            o += 1
            if o > (screens - 1):
                o = 0
            added = 0
        if "\n" in i:
            while o < screens and (o != 0 or strings[o][-1] != " "):
                strings[o] += [" "]
                o += 1
            o = 0
            strings[o][-1] += i.split("\n")[1]
            added = len(i.split("\n")[1])
            sized = dc.GetTextExtent(strings[o][-1]).x
            if sized > maxadd:
                maxadd = sized
        else:
            if strings[o][-1] != " ":
                strings[o][-1] += " " + i
            else:
                strings[o][-1] = i
            added += len(i)
            sized = dc.GetTextExtent(strings[o][-1]).x
            if sized > maxadd:
                maxadd = sized
    return strings, (maxadd + dc.GetTextExtent("_").x - 1) // dc.GetTextExtent("_").x

while True:
    try:
        laststring = ""
        while True:
            size = maxsize
            myFont.SetPointSize(size)
            dc.SetFont(myFont)
            contents = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/active").read())
            slides = []
            for i in contents["presentation"]["groups"]:
                for p in i["slides"]:
                    slides += [p["text"]]
            slideindex = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/slide_index").read())
            string = slides[slideindex["presentation_index"]["index"]].replace("\n", " \n")
            for i in range(screens):
                string = string.replace(f"From File Split{i + 1}.txt", "")
            if string == laststring:
                if os.name != "nt":
                    root.update()
                sleep(0.1)
                continue
            laststring = string
            strings, maxadd = main(string)
            for i in range(len(strings)):
                while strings[i][-1] == " " and len(strings[i]) != 1:
                    strings[i].pop()
            lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while y / dc.GetTextExtent("Test").y < lines:
                size -= 1
                myFont.SetPointSize(size)
                dc.SetFont(myFont)
                strings, maxadd = main(string)
                for i in range(len(strings)):
                    while strings[i][-1] == " " and len(strings[i]) != 1:
                        strings[i].pop()
                lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while dc.GetTextExtent("_" * maxadd).x > x // screens:
                size -= 1
                myFont.SetPointSize(size)
                dc.SetFont(myFont)
            for i in range(len(strings)):
                while len(strings[i]) < lines:
                    strings[i] += [" "]
                for p in range(len(strings[i])):
                    if strings[i][p] != " ":
                        strings[i][p] = strings[i][p].strip()
                if os.name == "nt":
                    strings[i] += ["_" * maxadd]
            if screens == 3:
                for i in range(len(strings[1])):
                    if strings[1][i] == " ":
                        strings[0][i], strings[1][i] = strings[1][i], strings[0][i]
            for i in range(screens):
                if os.name == "nt":
                    one = open(f"Split{i + 1}.txt", "w").write("\n".join(strings[i]))
                else:
                    T[i].delete("1.0", tk.END)
                    T[i].config(font = ("Arial", size))
                    T[i].insert(tk.END, "\n".join(strings[i]), "Just")
            sleep(0.1)
    except Exception:
        pass
