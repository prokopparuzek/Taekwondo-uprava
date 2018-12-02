#!/usr/bin/python3

import re,sys
from unidecode import unidecode

def uprav(csv, turnaj):
    csv = re.sub(r'([A-Z]{2,3})\n', r'\1', csv)
    csv = csv.split('\n')
    patS = r'^(Male|Female)'
    patC = r'Category:;*([^/]*)'
    patM = r'^;\d'
    fs = ';'
    out = []
    for line in csv:
        if re.search(patS, line):
            sex = re.search(patS, line).group(0)
        elif re.search(patC, line):
            cat = re.search(patC, line).group(1).rstrip()
        elif re.match(patM, line):
            mem = re.search(r'^;*([0-9]+).*\(([0-9]+)\);*([^;]+);*([A-Z]+);+([^;]+);*$', line)
            data = []
            for i in range(1,6):
                data.append(mem.group(i))
            out.append(cat + fs + sex + fs + price(data[0]) + fs + Wprice(data[1]) + fs + data[2] + fs + data[3] + fs + unidecode(data[4]) + fs + turnaj + fs + Aprice(data[0:2]))
    return out

def price(mista):
    bod = 0
    if mista == '1':
        bod += 5
    elif mista == '2':
        bod += 3
    elif mista == '3':
        bod += 1
    return str(bod)

def Wprice(data):
    bod = int(data) * 2
    return str(bod)

def Aprice(data):
    bod = int(price(data[0])) + int(Wprice(data[1]))
    return str(bod)

if __name__ == "__main__":
    coding = "utf-8"
    with open(sys.argv[1], mode="r", encoding=coding) as i:
        csv = i.read()
        out = uprav(csv, sys.argv[3])
    with open(sys.argv[2], mode="w", encoding=coding) as o:
        for line in out:
            o.write(line + '\n')
