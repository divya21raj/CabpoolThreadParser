import os
import json

def writeToJSONFile(fileName, data):
    path = os.path.dirname(os.path.realpath(__file__))
    filePathNameWExt = path + "/" + fileName + '.json'
    with open(filePathNameWExt, 'w+') as fp:
        json.dump(data, fp)

def writeToFIle(id):
    path = os.path.dirname(os.path.realpath(__file__))
    
    f = open(path + "/lastId.txt", "w+")
    f.write(id)
    f.close()

def checkNew(emailId):
    path = os.path.dirname(os.path.realpath(__file__))
    
    try:
        f = open(path + "/lastId.txt", "r+")
        data = f.read()
        if data == emailId:
            f.close
            print "duplicate"
            return False
        else:
            f.close()
            writeToFIle(emailId)
            return True
    except: 
        writeToFIle(emailId)
        return True
    
