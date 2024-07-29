import wx
import json
import urllib.request
from time import sleep

app = []; app = wx.App(None)
dc = wx.ScreenDC()
size = 250
myFont = wx.Font(size, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True)
dc.SetFont(myFont)

def main(string):
    strings = [[""], [""], [""]]
    splitstring = string.split(" ")
    o = 0
    added = 0
    for i in splitstring:
        if dc.GetTextExtent(strings[o][-1] + " " + i).x > 1280 and added > 0:
            strings[o] += [" "]
            o += 1
            if o > 2:
                o = 0
            added = 0
        if "\n" in i:
            while o < 3 and (o != 0 or strings[o][-1] != " "):
                strings[o] += [" "]
                o += 1
            o = 0
            strings[o][-1] += i.split("\n")[1]
            added = len(i.split("\n")[1])
        else:
            if strings[o][-1] != "" and strings[o][-1] != " ":
                strings[o][-1] += " " + i
            else:
                strings[o][-1] = i
            added += len(i)
    return strings

while True:
    try:
        laststring = ""
        while True:
            size = 250
            myFont.SetPointSize(size)
            dc.SetFont(myFont)
            contents = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/active").read())
            slides = []
            for i in contents["presentation"]["groups"]:
                for p in i["slides"]:
                    slides += [p["text"]]
            slideindex = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/slide_index").read())
            string = slides[slideindex["presentation_index"]["index"]].replace("\n", " \n")
            string = string.replace("From File Split1.txt", "")
            string = string.replace("From File Split2.txt", "")
            string = string.replace("From File Split3.txt", "")
            if string == laststring:
                sleep(0.1)
                continue
            laststring = string
            strings = main(string)
            lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while 2160 / dc.GetTextExtent("Test").y < lines:
                size -= 1
                myFont.SetPointSize(size)
                dc.SetFont(myFont)
                strings = main(string)
                lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            for i in range(0, len(strings)):
                while len(strings[i]) < lines:
                    strings[i] += [" "]
                for p in range(0, len(strings[i])):
                    if strings[i][p] != " ":
                        strings[i][p] = strings[i][p].strip()
            one = open("Split1.txt", "w").write("\n".join(strings[0]))
            two = open("Split2.txt", "w").write("\n".join(strings[1]))
            three = open("Split3.txt", "w").write("\n".join(strings[2]))
            sleep(0.1)
    except Exception:
        pass
