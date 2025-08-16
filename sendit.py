import requests
import threading
import string
import random
import os
os.system('title SendIt Spammer      [github.com/0vm/SendIt-auto]')

url = input('SendIt URL? ')
message = input('Enter Message: ')
threads = int(input('Threads 1 = slow, 20 = fast (Slow Reccomended): '))


tempmsg = message
message = ''
for c in tempmsg:
    message += c
    message += '\u200E'




def randomString(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def randomID():
    return randomString(8) + '-' + randomString(4) + '-' + randomString(4) + '-' + randomString(4) + '-' + randomString(12)

id = url.split('/')[4]
postId = None
if '?' in id:
    postId = id.split('?postId=')[1].split('&')[0] 
    id = id.split('?')[0]
headers = {"app-version": "1.0", "app-id": 'c2ad997f-1bf2-4f2c-b5fd-83926e8f3c65'}
response = requests.get('https://api.getsendit.com/v1/stickers/' + id + '?user=null&shadowToken=', headers=headers).json()

def content():

    obj = {
        "recipient_identity": {
            "type": "id",
            "value": response['payload']['sticker']['author']['id']
        },
        "type": "sendit.post-type:question-and-answer-v1",
        "data": {
            "question": message + ' ' + randomString(4),
        },
        "ext_data": {
            "sticker_id": id,
            "author_shadow_token": randomID()
        },
        "timer": 0
    }
    if postId != None:
        obj['ext_data']['reply_post_id'] = postId
    return obj

sent = 0

class sendThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        if threadID < 10:
            self.threadID = '0' + str(threadID)
        else:
            self.threadID = str(threadID)
    def run(self):
        global sent
        while True:
            try:
                status = requests.post('https://api.getsendit.com/v1/posts', json=content(), headers=headers).json()['status']
                if status == 'success':
                    os.system('title SendIt Spammer      [Sent: ' + str(sent) + ']      https://github.com/0vm/SendIt-Spammer')
                    sent += 1
            except:
                print('[' + self.threadID + '] ERROR, After ' + str(sent) + ' messages sent.')




for x in range(threads):
    thread = sendThread(x + 1)
    thread.start()
