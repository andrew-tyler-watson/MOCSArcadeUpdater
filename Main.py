from google_drive_downloader import GoogleDriveDownloader as gdd
import pymongo
import time
import sys
import os

#read parameters from the command line
#store in args
#the 1st parameter passed in must the path to the
#games directory

args = sys.argv[1:]

root = args[0]
if not os.path.exists(root):
    print("Warning!!! The root path being passed to the updater ")
    exit(-1)

def UpdateGames():
    #grab records
    records = []
    for record in records:
        if record.Inactive:
            DeleteGame(record)
        elif IsNewGame(record):
            DownloadGame(record)
            MarkAsUpdated(record)
            print('hello')
        elif record.shouldUpdate:
            UpdateGame(record)
            MarkAsUpdated(record)
def DeleteGame(record):
    #find the game folder
    #delete it
    print('hello')

def UpdateGame(record):
    DeleteGame(record)
    DownloadGame(record)

def DownloadGame(record):
    path = os.path.join(root, 'Easy68K.zip')

    gdd.download_file_from_google_drive(file_id='1ePTrCLOmyojyXAD5KlSotBPPCl2ei-GO',
                                        dest_path=path,
                                        unzip=True,
                                        overwrite=True)

def MarkAsUpdated(record):
    print('Mark as Updated')

def IsNewGame(record):
    print('Hello')

# if len(args) == 1:
#     while(True):
#         time.sleep(600)
#         UpdateGames()
# if len(args) > 1:
#     print()
#     UpdateGame(args[0])

DownloadGame(0)