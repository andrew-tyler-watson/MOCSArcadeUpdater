# this package downloads and unzips our games
from google_drive_downloader import GoogleDriveDownloader as gdd
# this is our mongo client
from pymongo import MongoClient
# time related stuff
import time
# this package let's us get command line args
import sys
# this package provides OS independent
# wrappers for paths and file manipulation
import os
# this package is used to delete
# directories and all of their contents
import shutil

#read parameters from the command line
#store in args
#the 1st parameter passed in must the path to the
#games directory

ROOT = ''

def main():
    args = sys.argv[1:]
    globals()['ROOT'] = args[0]
    db = ConnectAndReturnDatabase()
    if not os.path.exists(ROOT):
        print("Warning!!! The root path being passed to the updater ")
        exit(-1)
    if len(args) == 1:
        UpdateGames(db)
    if len(args) > 1:
        collection = db['games']
        game = collection.find({'name': args[1]})
        for record in game:
            if record['shouldUpdate']:
                UpdateGame(record)

def UpdateGames(db):
    #grab records
    collection = db['games']
    records = collection.find({})
    # for record in records:
    #     print(record)
    for record in records:
        if GameIsPresent(record['name']):
            if record['shouldUpdate']:
                UpdateGame(record)
                continue
        if not record['isActive']:
            if GameIsPresent(record['name']):
                DeleteGame(record)
                collection.delete_one({'name': record['name']})
                continue
        if not GameIsPresent(record['name']):
            if record['isActive']:
                DownloadGame(record)
                DeleteZip(record['name'])
                continue




        # if not  and GameIsPresent(record['name']):
        #
        # elif record['shouldUpdate']:
        #     UpdateGame(record)
        #     # Mark as updated
        #     collection.update_one({'_id': record.get('_id')}, {'$set': {'shouldUpdate': False}})
        # elif not GameIsPresent(record['name']):
        #


def DeleteGame(record):
    #find the game folder
    #delete it
    FolderPath = os.path.join(ROOT,  record['name'])
    shutil.rmtree(FolderPath)

def DeleteZip(GameName):
    FilePath = os.path.join(ROOT,  GameName + '.zip')
    os.remove(FilePath)

def UpdateGame(record):
    DeleteGame(record)
    DownloadGame(record)
    DeleteZip(record['name'])

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
        if str(dir) == gameName:
            print(gameName + " found")
            return True
    return False

if __name__ == "__main__":
    main()