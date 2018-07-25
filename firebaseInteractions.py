
import pyrebase
import os


def initFirebase():
    config = {
        "apiKey": "AIzaSyAbviwwtxjwpZyiqvRzzulh6YycC11F1vQ",
        "authDomain": "snu-cabpool-db611.firebaseapp.com",
        "databaseURL": "https://snu-cabpool-db611.firebaseio.com",
        "storageBucket": "snu-cabpool-db611.appspot.com",
        "serviceAccount": os.path.dirname(os.path.realpath(__file__)) + "google-services.json"
        }
        
    return pyrebase.initialize_app(config)
