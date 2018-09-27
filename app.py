from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json
import errno
import os
import sys, random
import tempfile
import requests
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('t5b5X0LHwCZQHy55X75+FZfjBWBDfvw+NWgDIruLX/EoslSALtJHPdaBsVRlkjFUeQRscNzXPtkTI8dYZH6I+ku1yyGazFjq8KShojdmcowVeXZYWNjkd7oT5nAxHZIK8q+lM/KR0DM+IwdyO5lyGQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b38e05865272e44156c19da5d5191c83')

#===========[ NOTE SAVER ]=======================
notes = {}
# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
    if text=="adit":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu jahat adit'))
    if text=="rey":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Apa?'))
    if text=="test":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='?'))
    if text=="ip 4":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Andhika'))
    if text=="AudioMessage":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Andhika'))
    if text=="mail":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu jahat mail'))
    if text=="djohan":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu jahat djohan'))
    #line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.user_id+' '+profile.display_name+'\nKata Kunci Tidak Diketahui :) \nKetik "menu" untuk mengetahui menu yang tersedia'))
    line_bot_api.push_message('U8d343d76a1c15caad6dba2d2b5dab241', TextSendMessage(text='Hello World!'))

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
