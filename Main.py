from google_drive_downloader import GoogleDriveDownloader as gdd
from pymongo import MongoClient
import time
import sys
import os

#read parameters from the command line
#store in args
#the 1st parameter passed in must the path to the
#games directory

ROOT = ''

def main():
    args = sys.argv[1:]
    globals()['ROOT'] = args[0]

    if not os.path.exists(ROOT):
        print("Warning!!! The root path being passed to the updater ")
        exit(-1)
    if len(args) == 1:
        while(True):
            db = ConnectAndReturnDatabase()
            UpdateGames(db)
            time.sleep(600)
    if len(args) > 1:
        print()
        UpdateGame(args[1])

def UpdateGames(db):
    #grab records
    collection = db['games']
    records = collection.find({})
    # for record in records:
    #     print(record)
    for record in records:
        if record['shouldUpdate']:
            UpdateGame(record)
            # Mark as updated
            collection.update_one({'_id': record.get('_id')}, {'$set': {'shouldUpdate': False}})
        elif not GameIsPresent(record['name']):
            print("not present")
        else:
            DeleteGame(record.name)

def DeleteGame(record):
    #find the game folder
    #delete it
    print('hello')

def UpdateGame(record):
    DeleteGame(record)
    DownloadGame(record)

def DownloadGame(record):
    # combine the root path with the name of the game and the extension of what we are expecting
    path = os.path.join(ROOT, record['name'] + '.zip')
    print(path)
    #let our package do the hard work and have it unzip our zip and overwrite anything in the way
    gdd.download_file_from_google_drive(file_id=record['fileId'],
                                        dest_path=path,
                                        unzip=True,
                                        overwrite=True)

def ConnectAndReturnDatabase():
    client = MongoClient('mongodb+srv://MOCSArcade2:Hamburger69@cluster0-xczcq.gcp.mongodb.net/MOCSArcade?retryWrites=true&w=majority')
    return client.MOCSArcade

def GameIsPresent(gameName):
    for dir in os.listdir(ROOT):
        if dir == gameName:
            print(gameName + " found")
            return True

if __name__ == "__main__":
    main()