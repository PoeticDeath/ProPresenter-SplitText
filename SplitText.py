import json
import urllib.request
from time import sleep
while True:
    try:
        laststring = ""
        while True:
            contents = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/active").read())
            slides = []
            for i in contents["presentation"]["groups"]:
                for p in i["slides"]:
                    slides += [p["text"]]
            slideindex = json.loads(urllib.request.urlopen("http://127.0.0.1:1025/v1/presentation/slide_index").read())
            string = slides[slideindex["presentation_index"]["index"]].replace("\n", " \n")
            if string == laststring:
                sleep(0.1)
                continue
            laststring = string
            strings = [[""], [""], [""]]
            splitstring = string.split(" ")
            o = 0
            added = 0
            for i in splitstring:
                if added + len(i) > 7 and added > 0:
                    strings[o] += [" "]
                    o += 1
                    if o > 2:
                        o = 0
                    added = 0
                if "\n" in i:
                    while o < 3 and o != 0:
                        strings[o] += [" "]
                        o += 1
                    o = 0
                    strings[o][-1] += i.split("\n")[1]
                    added = len(i.split("\n")[1])
                else:
                    if strings[o][-1] != "":
                        strings[o][-1] += " " + i
                    else:
                        strings[o][-1] = i
                    added += len(i)
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
