# -*- coding:utf-8 -*-
from psd_tools import PSDImage
import os
import json

# psd.composite().save("./images/超值礼包新增2.png")

# TypeLayer is a layer with texts:

fontSet = set()
psdInfo = []
psdFileName = ""


def getTypeLayer(Layers):
    global fontSet
    global psdInfo
    global psdFileName

    for layer in Layers:
        if layer.is_group():
            getTypeLayer(layer)
        elif layer.__class__.__name__.lower() == "typelayer":
            text = layer.engine_dict['Editor']['Text'].value
            fontset = layer.resource_dict['FontSet']
            runlength = layer.engine_dict['StyleRun']['RunLengthArray']
            rundata = layer.engine_dict['StyleRun']['RunArray']
            for _, style in zip(runlength, rundata):
                info = {"psd": psdFileName, "text": "",
                        "font": "", "fontSize": 0, "fontColor": ""}
                substring = text
                info["text"] = text
                stylesheet = style['StyleSheet']['StyleSheetData']
                if stylesheet.get('Font') != None:
                    font = fontset[stylesheet['Font']]
                    fontSet.add(font["Name"])
                    info["font"] = str(font["Name"])[1:-1]
                print("text: ", substring)
                # print("font: ", font["Name"])

                # print("fontSize: ", stylesheet["FontSize"])
                if stylesheet.get('FillColor') != None:
                    ARGB = stylesheet["FillColor"]["Values"]
                    RGB = {"R": round(
                        ARGB[1]*255), "G": round(ARGB[2]*255), "B": round(ARGB[3]*255)}
                    info["fontColor"] = RGB
                    # print(RGB)
                # print()
                psdInfo.append(info)
                break


for _, _, files in os.walk("./"):
    for file in files:
        if file.lower().endswith(".psd"):
            psdFileName = file
            psd = PSDImage.open(file)
            getTypeLayer(psd)

# psd = PSDImage.open("./超值礼包新增2.psd")
# getTypeLayer(psd)
f = open("fonts.txt", "w")
for i in fontSet:
    # print(i)
    f.write(str(i)[1:-1])
    f.write("\n")
f.close()

f = open("psd info.json", "w", encoding='utf8')
f.write(json.dumps(psdInfo, ensure_ascii=False))
f.close()
