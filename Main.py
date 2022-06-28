import requests as req
import json
import os
import multiprocessing

#OPEN BROWSER AND LOGIN TO DISCORD

#autorization token, catch via dev mod of browser
#best in "typing" post request, but can be anywhere
authorization = ''
#channel id is last part of url
channel_id = ''
#only for naming output folder
channel_name = ''



#Fetch whole chat to json, this take some time.
def message_fetch(auth, channel_id):

    #way to send autorized request
    headers = {
        'authorization' : auth
    }
    r = req.get(
        f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)

    #request to json variable    
    js = json.loads(r.text)
    last = 0
    
    #Discord give back only 50 last messages, this is way how iter to past
    while (js[-1]['id'] != last):
        last = js[-1]['id']
        print(js[-1]['timestamp'])
        #Print every 50th creation date of message, just for debbug.
        r = req.get(
            f'https://discord.com/api/v9/channels/{channel_id}/messages?before={last}&limit=50', headers=headers)
        js += json.loads(r.text) #Concat to js
    return js

#Parallel downloading
def para_img_get(data):
    # grep right data with key
    preurl = data['attachments']
    # not always there are attachmens
    if len(preurl) > 0:
        # Output is two dimensinal for some reason 
        urlToDownload = preurl [0]['url']
        # File name assemble
        suffix = os.path.splitext(urlToDownload)[1]
        nameForFile = urlToDownload.split("/")[-2]
        ComplexPathForFile = f'{channel_name}/{nameForFile+suffix}'
        # and request and save file
        if not os.path.isfile(ComplexPathForFile):
            r = req.get(urlToDownload)
            with open (ComplexPathForFile, 'wb') as fi:
                fi.write(r.content)
            print(ComplexPathForFile)

#Main function of download
def download_images():
    #Create folder for download
    if not os.path.isdir(channel_name):
        os.mkdir(channel_name)

    #Open and load fetched chat
    f = open('mess.json')
    data = json.load(f)
    
    #serial iter is slow so I make it parallel
    pool_obj = multiprocessing.Pool()

    pool_obj.map(para_img_get,data)
    f.close()


#call of message fetch
jso = message_fetch(authorization, channel_id)
#save to json
with open('mess.json', 'w') as f:
    json.dump(jso, f)
#and download    
download_images()
