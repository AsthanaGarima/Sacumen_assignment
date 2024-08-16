from tkinter import filedialog
from tkinter import *
import os
import imageio as iio
import boto
import boto.s3
from boto.s3.key import Key
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

def upload_to_google(testfile):
    
    credentials_dict = {
        'type': 'service_account',
        'client_id': os.environ['BACKUP_CLIENT_ID'],
        'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
        'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
        'private_key': os.environ['BACKUP_PRIVATE_KEY'],
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict
    )
    client = storage.Client(credentials=credentials, project='myproject')
    bucket = client.get_bucket('mybucket')
    blob = bucket.blob(testfile)
    blob.upload_from_filename(testfile)

def upload_to_s3(testfile):
    s3_connection = boto.connect_s3()
    bucket = s3_connection.get_bucket('bucket1')
    key = boto.s3.key.Key(bucket, testfile)
    with open(testfile) as f:
        key.send_file(f)

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    arr = os.listdir(filename)
    print(arr)
    for val in arr:
        if val.find('.txt') or val.find('.pdf') or val.find('.xlsx')>1 or val.find('.doc') or val.find('.docx') or val.find('.csv'):
            upload_to_s3(filename+"/"+val)
        elif val.find('.mp3') or val.find('.mp4')>1 or val.find('.png') or val.find('.jpg') or val.find('.jpeg')or val.find('.svg')or val.find('.mpeg4') or val.find('.wmv') or val.find('.3gp') or val.find('webm'):
            upload_to_google(filename+"/"+val)
       

        

root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)

mainloop()