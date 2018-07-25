
import pyrebase
import os


def isValid(mailMap):
    if not mailMap.has_key('time'):
        return False
    elif mailMap.get("phone") == '' and mailMap.get("email") == '':
        return False
    
    return True

def initFirebase():
    config = {
        "apiKey": "AIzaSyAbviwwtxjwpZyiqvRzzulh6YycC11F1vQ",
        "authDomain": "snu-cabpool-db611.firebaseapp.com",
        "databaseURL": "https://snu-cabpool-db611.firebaseio.com",
        "storageBucket": "snu-cabpool-db611.appspot.com",
        "serviceAccount": os.path.dirname(os.path.realpath(__file__)) + "/service_cred.json"
        }
        
    return pyrebase.initialize_app(config)

def pushMap(mailMap):
    firebase = initFirebase()
    db = firebase.database()

    if isValid(mailMap):
        rec = db.child('mega_entries').push(mailMap)
        db.child('mega_entries').child(rec['name']).update({"entry_id":rec['name']})

    print rec