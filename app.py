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
def carimhs(nmr):
    URLmhs = "http://www.aditmasih.tk/api_andhika/show.php?nmr=" + nmr
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nmr = data['data_angkatan'][0]['nmr']
        sangar = data['data_angkatan'][0]['sangar']
    
        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Kesangaran ke-"+nmr+"\n"+sangar
        return data
        # return all_data

    elif(flag == "0"):
        return err

def cari(jawa):
    URLmhs = "http://www.aditmasih.tk/jaw/show.php?jawa=" + jawa
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        jawa = data['data_angkatan'][0]['jawa']
        indo = data['data_angkatan'][0]['indo']
    
        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= jawa+" : "+indo
        return data
        # return all_data

    elif(flag == "0"):
        return err
#INPUT DATA MHS
def inputmhs(nmr, sangar):
    r = requests.post("http://www.aditmasih.tk/api_andhika/insert.php", data={'nmr': nmr, 'sangar': sangar})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def inputput(jawa, indo):
    r = requests.post("http://www.aditmasih.tk/jaw/insert.php", data={'jawa': jawa, 'indo': indo})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allmhs():
    r = requests.post("http://www.aditmasih.tk/api_andhika/all.php")
    data = r.json()
    flag = data['flag']
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_angkatan'])):
            nmr = data['data_angkatan'][int(i)][0]
            sangar = data['data_angkatan'][int(i)][2]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nKesangaran ke "
            hasil=hasil+nmr
            hasil=hasil+"\n"
            hasil=hasil+sangar
            hasil=hasil+"\n"
        return hasil

def bingung(x):
    return x[::-1]

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
    teks = event.message.text
    text = teks.lower().strip()
    data=text.split('-')
    data2=text.split(' ')
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

#MENAMPILKAN MENU
    if text=="/menu":
        menu="1. '/sangar' gawe ndelok kesangaran wong-wong\n2. '/spam-[kalimat]-[jumlah spam]' gawe nyepam wong sing mbok sayang\n3. '/spamkata [kalimat]' gawe nyepam tiap kata sebanyak kalimat sing diketik\n4. '/bye' gawe ngetokno bot teko grup opo room\n5. '/rev-[kalimat]' gawe ngewalik tulisan\n6. '/dev' ndelok pengembang bot line iki\n7. tiap ngetik ng grup opo room isok munculo terjemahan boso jowo\n\nawakmu bebas isok ngetik keyword nggawe huruf gede opo cilik"  
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))

#PENGEMBANGAN
    if text=="rey":
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png',preview_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png'))
    if text=="Google Center":
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='Mountain View, California', address='United State of America',latitude=37.4225195,longitude=-122.0847433))

#MENU SANGAR
    elif(data[0]=='/sangar'):
        pro = "Wong suroboyo terkenal karo kesangarane. Sak piro sangarmu cak?\n1. lihat-[id]\n2. tambah-[id]-[kesangaran]\n3. hapus-[id]\n4. ganti-[id lama]-[id baru]-[kesangaran baru]\n5. kabeh"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=pro))

#SUB MENU SANGAR
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    elif(data[0]=='kabeh'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allsmhs()))

    elif(data[0]=='kamus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputput(data[1],data[2])))

#SPAM
    elif (data[0]=='/spam'):
        i = 0
        if(int(data[2])>1000):
            if isinstance(event.source, SourceGroup):
                line_bot_api.push_message(event.source.group_id,TextSendMessage(text="kakean woi, nggarakno server lemot ae"))
            elif isinstance(event.source, SourceRoom):
                line_bot_api.push_message(event.source.room_id,TextSendMessage(text="kakean woi, nggarakno server lemot ae"))
        else:
            while i < int(data[2]):
                if isinstance(event.source, SourceGroup):
                    line_bot_api.push_message(event.source.group_id,TextSendMessage(text=data[1]))
                elif isinstance(event.source, SourceRoom):
                    line_bot_api.push_message(event.source.room_id,TextSendMessage(text=data[1]))
                #else:
                #   line_bot_api.push_message(event.source.user_id,TextSendMessage(text=data[1]))
                i =i+1
    elif text =="/apa":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png', title='this is menu1', text='description1', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='message1',text='message text1'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png', title='this is menu1', text='description1', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='message1',text='message text1'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png', title='this is menu1', text='description1', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='message1',text='message text1'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png', title='this is menu1', text='description1', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='message1',text='message text1'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png', title='this is menu1', text='description1', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='message1',text='message text1'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://azurlane.koumakan.jp/w/images/d/d8/San_Diego.png',title='this is menu2',text='description2',
                    actions=[
                        PostbackAction(label='postback2',text='postback text2',data='action=buy&itemid=2'),
                        MessageAction(label='message2',text='message text2'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')])
                    ]
                )
            )
        )
    elif text =="/dev":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://andhikay24.000webhostapp.com/IMG_20180805_103128.jpg',
            title='PENGEMBANG',
            text='Andhika Yoga Perdana, Mahasiswa Informatika ITS',
            actions=[
                PostbackAction(
                    label='Submenu saat ini',
                    text='/dev',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='Kembali ke menu',
                    text='/menu'
                ),
                URIAction(
                    label='My Personal Website',
                    uri='http://andhikay24.000webhostapp.com/'
                )
            ]
        )
    ))

    #TINGGALKAN GROUP/ROOM
    elif text=="/bye":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Pingin ngekick aku?:(\nketik "/start" gawe ngekick!'))
    elif text=="/start":
        if isinstance(event.source, SourceGroup):
            line_bot_api.push_message(event.source.group_id, TextSendMessage(text='Woy '+profile.display_name+', kurang ajar banget kon wani ngekick aku teko grup iki!'))
            line_bot_api.push_message(event.source.room_id, TextSendMessage(text='Sepurane rek aku tinggal disek, aku bosen ng kene! GAK MENARIK blass cuk'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.push_message(event.source.room_id, TextSendMessage(text='Woy '+profile.display_name+', kurang ajar banget kon wani ngekick aku teko grup iki!'))
            line_bot_api.push_message(event.source.room_id, TextSendMessage(text='Sepurane rek aku tinggal disek, aku bosen ng kene! GAK MENARIK blass cuk'))
            line_bot_api.leave_room(event.source.room_id)
        else: 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Mending blokiren aku daripada ngekick aku"))
    
#CHAT 1:1
    #elif not(isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom)):
     #   line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hai,' +profile.display_name+'. Bahasa opo iki?\n'+event.message.text+'\nKok gak jelas banget'))
    
    #line_bot_api.multicast(['U8d343d76a1c15caad6dba2d2b5dab241'], TextSendMessage(text='Selamat Siang!'))
    elif (data2[0]=='/spamkata'):
        x=1
        while  x <= len(data2):
            if isinstance(event.source, SourceRoom):
                line_bot_api.push_message(event.source.room_id,TextSendMessage(text=data2[x]))
            elif isinstance(event.source, SourceGroup):
                line_bot_api.push_message(event.source.group_id,TextSendMessage(text=data2[x]))
            else:
                line_bot_api.push_message(event.source.user_id,TextSendMessage(text=data2[x]))
            x=x+1 
    
    elif (data[0]=='/rev'):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=bingung(data[1])))

   # x=0
    #while  x <= len(data2):
     #   if isinstance(event.source, SourceRoom):
      #      line_bot_api.push_message(event.source.room_id,TextSendMessage(text=cari(data2[x])))
       # elif isinstance(event.source, SourceGroup):
        #    line_bot_api.push_message(event.source.group_id,TextSendMessage(text=cari(data2[x])))
        #else:
            #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=cari(data2[x])))
        #x=x+1     

#kicker.kickoutFromGroup(msg.to,[target])
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

#KENAPA KOK CUMAN TIPE INTEGER
#KENAPA JAW GK ADA FITUR HAPUS
#GMN BIAR GK MERETURN APAPUN
