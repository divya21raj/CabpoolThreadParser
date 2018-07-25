import re
import json
import os


def getDelim(content):
    hyphenCount = 0
    colonCount = 0

    for line in content:
        hyphenCount += line.count("-")
        colonCount += line.count(":")

    if hyphenCount > colonCount:
        return "-"
    else: return ":"

def getPhone(line):
    for word in re.findall(r"[\w']+", line):
        match = re.search(r"^[6-9]\d{9}$", word.strip()) 
        if match:
            return match.group()
    return ""

def getValue(line, delim, key):
    line = line.replace(delim, "?", 1)
    delim = "?"
    
    for word in line.split(delim):
        word = word.strip()
        if word.lower() != key: return word

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = fileName + '.json'
    with open(filePathNameWExt, 'w+') as fp:
        json.dump(data, fp)

def parse():
    with open("data.txt") as file:
        content = file.readlines()

    delim = getDelim(content)
    print delim

    phone = ""
        
    for line in content:
        if "to" in line.replace(" ", "").lower().split(delim):
            destination = getValue(line, delim, "to")
            print "Destination = " + destination

        elif "from" in line.replace(" ", "").lower().split(delim):
            source = getValue(line, delim, "from")
            print "Source = " + source

        elif "date" in line.replace(" ", "").lower().split(delim):
            date = getValue(line, delim, "date")
            print "Date = " + date

        elif "time" in line.replace(" ", "").lower().split(delim):
            time = getValue(line, delim, "time")
            print "Time = " + time
        
        elif phone == "" :
            phone = getPhone(line)
            
            if phone != "":
                print "Phone = " + phone


    mailJson = {}
    mailJson['phone'] = phone
    mailJson['destination'] = {'latitide': 0, 'longitude': 0, 'name': destination}
    mailJson['source'] = {'latitide': 0, 'longitude': 0, 'name': source}
    mailJson['time'] = time
    mailJson['date'] = date
    mailJson['notFromApp'] = 'true'

    dirPath = os.path.dirname(os.path.realpath(__file__))

    writeToJSONFile(dirPath,'mail',mailJson)
        
    return mailJson
