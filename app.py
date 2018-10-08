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

#REQUEST DATA MHS
def carimhs(nrp):
    URLmhs = "http://www.aditmasih.tk/api-hafid/show.php?nrp=" + nrp
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nrp = data['data_angkatan'][0]['nrp']
        nama = data['data_angkatan'][0]['nama']
        kos = data['data_angkatan'][0]['kosan']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Nama : "+nama+"\nNrp : "+nrp+"\nKosan : "+kos
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA MHS
def inputmhs(nrp, nama, kosan):
    r = requests.post("http://www.aditmasih.tk/api-hafid/insert.php", data={'nrp': nrp, 'nama': nama, 'kosan': kosan})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allmhs():
    r = requests.post("http://www.aditmasih.tk/api-hafid/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_angkatan'])):
            nrp = data['data_angkatan'][int(i)][0]
            nama = data['data_angkatan'][int(i)][2]
            kos = data['data_angkatan'][int(i)][4]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nNrp : "
            hasil=hasil+nrp
            hasil=hasil+"\nNama : "
            hasil=hasil+nama
            hasil=hasil+"\nKosan : "
            hasil=hasil+kos
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'


#DELETE DATA MHS
def hapusmhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api-hafid/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatemhs(nrpLama,nrp,nama,kosan):
    URLmhs = "http://www.aditmasih.tk/api-hafid/show.php?nrp=" + nrpLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama=nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api-hafid/update.php", data={'nrp': nrp, 'nama': nama, 'kosan': kosan, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+'berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err

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
        inia="Hypertext"
        inib="telolet"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=inia+inib))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=inib))
    if text=="rey":
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png',preview_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png'))
    if text=="Google Center":
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='Mountain View, California', address='United State of America',latitude=37.4225195,longitude=-122.0847433))
    
    data=text.split('-') #pemisah
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    elif(data[0]=='semwa'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allsmhs()))
    elif(data[0]=='menu'):
        menu = "1. lihat-[nrp]\n2. tambah-[nrp]-[nama]-[kosan]\n3. hapus-[nrp]\n4. ganti-[nrp lama]-[nrp baru]-[nama baru]-[kosan baru]\n5. semwa"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))
    elif text=="/bye":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Pingin ngekick aku?:(\nketik "/start" gawe ngekick!'))
        if text=="/start":
            if isinstance(event.source, SourceGroup):
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='woy '+profile.display_name+', kurang ajar banget kon wani ngekick aku teko grup iki!'))
                line_bot_api.leave_group(event.source.group_id)
            elif isinstance(event.source, SourceRoom):
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='sepurane rek aku tinggal disek, aku bosen ng kene! GAK MENARIK blass cuk'))
                line_bot_api.leave_room(event.source.room_id)
            else: 
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Mending blokiren aku daripada ngekick aku"))
    elif isinstance(event.source, SourceGroup) and isinstance(event.source, SourceRoom):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hai,' +profile.display_name+'. Kata kunci "'+event.message.text+'" belum tersedia. Ketik "menu" untuk menampilkan semua kata kunci yang ada'))
    #line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.user_id+' '+profile.display_name+'\nKata Kunci Tidak Diketahui :) \nKetik "menu" untuk mengetahui menu yang tersedia'))
    #line_bot_api.push_message('U8d343d76a1c15caad6dba2d2b5dab241', TextSendMessage(text='Hello World!'))
    #line_bot_api.multicast(['U8d343d76a1c15caad6dba2d2b5dab241'], TextSendMessage(text='Selamat Siang!'))

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
