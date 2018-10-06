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
#import datetime
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
    if text=="HTML":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hypertext Markup Language'))
    if text=="CSS":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Cascading Style Sheet'))
    if text=="ROM":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Read Only Memory'))
    if text=="RAM":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Random Access Memory'))
    if text=="API":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Application Programming Interface'))
    if text=="DNS":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Domain Name System'))
    if text=="HTTP":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hypertext Transfer Protocol'))
    if text=="SEM":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Search Engine Marketing'))
    if text=="SEO":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Search Engine Optimization'))
    if text=="rey":
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png',preview_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png'))
    if text=="ITS":
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='my location', address='ITS',latitude=-7.281476,longitude=112.794884))
    if text=="bye":
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Leaving multiple chat room'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Bot can't leave from 1:1 chat"))

    #line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.user_id+' '+profile.display_name+'\nKata Kunci Tidak Diketahui :) \nKetik "menu" untuk mengetahui menu yang tersedia'))
    #line_bot_api.push_message('U8d343d76a1c15caad6dba2d2b5dab241', TextSendMessage(text='Hello World!'))
    #line_bot_api.multicast(['U8d343d76a1c15caad6dba2d2b5dab241'], TextSendMessage(text='Selamat Siang!'))

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
