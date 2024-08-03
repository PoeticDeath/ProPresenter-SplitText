import wx
import json
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

def main(string):
    strings = [[" "] for i in range(screens)]
    splitstring = string.split(" ")
    o = 0
    added = 0
    maxadd = 0
    for i in splitstring:
        if ((dc.GetTextExtent(strings[o][-1] + " " + i).x > (x // screens) and added > 10) or (strings[o][-1].count(" ") > 2)) and strings[o][-1][-1] != "'":
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
                sleep(0.1)
                continue
            laststring = string
            strings, maxadd = main(string)
            for i in range(len(strings)):
                while strings[i][-1] == " ":
                    strings[i].pop()
            lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            while y / dc.GetTextExtent("Test").y < lines:
                size -= 1
                myFont.SetPointSize(size)
                dc.SetFont(myFont)
                strings, maxadd = main(string)
                for i in range(len(strings)):
                    while strings[i][-1] == " ":
                        strings[i].pop()
                lines = max(len(strings[0]), len(strings[1]), len(strings[2]))
            for i in range(len(strings)):
                while len(strings[i]) < lines:
                    strings[i] += [" "]
                for p in range(len(strings[i])):
                    if strings[i][p] != " ":
                        strings[i][p] = strings[i][p].strip()
                strings[i] += ["_" * maxadd]
            if screens == 3:
                for i in range(len(strings[1])):
                    if strings[1][i] == " ":
                        strings[0][i], strings[1][i] = strings[1][i], strings[0][i]
            for i in range(screens):
                one = open(f"Split{i + 1}.txt", "w").write("\n".join(strings[i]))
            sleep(0.1)
    except Exception:
        pass
