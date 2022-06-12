import requests as req
import json
import os

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



def download_images(folder_name):
    #Create folder for download
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    #Open and load fetched chat
    f = open('mess.json')
    data = json.load(f)
    #iter
    for i in data:
        # grep right data with key
        preurl = i['attachments']
        # not always there are attachmens
        if len(preurl) > 0:
            # Output is two dimensinal for some reason 
            urlToDownload = preurl [0]['url']
            # File name assemble
            suffix = os.path.splitext(urlToDownload)[1]
            nameForFile = urlToDownload.split("/")[-2]
            # and request and save file
            r = req.get(urlToDownload)
            with open (f'{folder_name}/{nameForFile+suffix}', 'wb') as fi:
                fi.write(r.content)
    f.close()


jso = message_fetch(authorization, channel_id)
with open('mess.json', 'w') as f:
    json.dump(jso, f)
download_images(channel_name)
