import json
import tkinter as tk
import urllib.request
from time import sleep
import tkinter.font as ft

x = 3840
y = 2160
screens = 3
maxsize = size = 250
fontf = "Arial"

root = tk.Tk()
root.config(bg = "systemTransparent")
root.wm_attributes("-transparent", 1)
root.overrideredirect(1)
root.wm_attributes("-topmost", 1)

font = ft.Font(font = (fontf, size))

T = []
for i in range(screens):
    T += [tk.Text(root)]
    T[i].config(bg = "systemTransparent", fg = "white", font = (fontf, size), borderwidth = 0, highlightthickness = 0, wrap = "none", state = "disabled")
    T[i].pack()
    T[i].place(x = (x // screens) * i, y = 0, width = x // screens, height = y)
    Just = "center"
    if i == 0:
        Just = "right"
    if i == screens - 1:
        Just = "left"
    T[i].tag_config("Just", justify = Just)

root.geometry(f"{x}x{y}+5760+0")

def main(string):
    strings = [[" "] for i in range(screens)]
    splitstring = string.split(" ")
    o = 0
    added = 0
    for i in splitstring:
        if ((font.measure(strings[o][-1] + " " + i + " ") > (x // screens) and added > 10) or (strings[o][-1].count(" ") > 2)) and strings[o][-1][-1] != "'":
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
        else:
            if strings[o][-1] != " ":
                strings[o][-1] += " " + i
            else:
                strings[o][-1] = i
            added += len(i)
    return strings

while True:
    try:
        laststring = ""
        while True:
            size = maxsize
            font = ft.Font(font = (fontf, size))
            contents = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/active").read())
            slides = []
            try:
                empty = "Not Split.pro" in contents["presentation"]["presentation_path"]
            except TypeError:
                empty = True
            announcementindex = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/announcement/slide_index?chuncked=false").read())
            if empty or announcementindex["announcement_index"] != None:
                laststring = string = ""
                for i in range(screens):
                    root.wm_attributes("-transparent", 0)
                    T[i].config(state = "normal")
                    T[i].delete("1.0", tk.END)
                    T[i].config(state = "disabled")
                    root.wm_attributes("-transparent", 1)
                root.update()
                sleep(0.1)
                continue
            for i in contents["presentation"]["groups"]:
                for p in i["slides"]:
                    slides += [p["text"]]
            slideindex = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/slide_index").read())
            string = slides[slideindex["presentation_index"]["index"]].replace("\n", " \n")
            if string == laststring:
                root.update()
                sleep(0.1)
                continue
            laststring = string
            strings = main(string)
            for i in range(len(strings)):
                while strings[i][-1] == " " and len(strings[i]) != 1:
                    strings[i].pop()
            lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while y / font.metrics("linespace") < lines:
                size -= 1
                font = ft.Font(font = (fontf, size))
                strings = main(string)
                for i in range(len(strings)):
                    while strings[i][-1] == " " and len(strings[i]) != 1:
                        strings[i].pop()
                lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while max([max([font.measure(o) for o in i]) for i in strings]) > x // screens:
                size -= 1
                font = ft.Font(font = (fontf, size))
            for i in range(len(strings)):
                while len(strings[i]) < lines:
                    strings[i] += [" "]
                for p in range(len(strings[i])):
                    if strings[i][p] != " ":
                        strings[i][p] = strings[i][p].strip()
            if screens == 3:
                for i in range(len(strings[1])):
                    if strings[1][i] == " ":
                        strings[0][i], strings[1][i] = strings[1][i], strings[0][i]
            for i in range(screens):
                root.wm_attributes("-transparent", 0)
                T[i].config(state = "normal")
                T[i].delete("1.0", tk.END)
                T[i].config(font = (fontf, size))
                T[i].insert(tk.END, "\n".join(strings[i]), "Just")
                T[i].config(state = "disabled")
                root.wm_attributes("-transparent", 1)
            sleep(0.1)
    except Exception:
        pass
