import os
from slack_bolt import App

import urllib.request as request
from PIL import Image
from io import BytesIO


response_callback = None

def set_callback(cb):
    global response_callback
    response_callback = cb

def getApp():
    token = os.environ.get('SLACK_BOT_TOKEN')
    secret = os.environ.get("SLACK_SIGNING_SECRET")
    if token is None or secret is None:
        return None
    app = App(
        token = token, 
        signing_secret = secret
    )
    
    @app.event('file_shared')
    def received_file(client, event, logger, say):
        try:
            file_id = event["file_id"]
        except KeyError:
            logger.error('No "file_id" field in response')
            return
        print(f'Received file id={file_id}')
        result = client.files_info(file=file_id)
        try:
            f = result['file']
            url = f["url_private_download"]
        except KeyError:
            logger.error('No file foumd in response')
            return
        print(f'Received file url={url}')
        img_req = request.Request(url, headers={'Authorization': 'Bearer %s' % token})
        img_data = request.urlopen(img_req).read()
        img = Image.open(BytesIO(img_data))
        if response_callback:
            say(response_callback(img))
    return app

def start():
    getApp().start(port=int(os.environ.get("SLACK_BOT_PORT", 3000)))

## 问题：
# 3. 接收者栏目里没有我的APP