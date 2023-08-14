#(©)Codexbotz
import aiohttp
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from plugins.data import ODD, EVEN ,BOTEFITMSG, FOMET, ZEE_KANNADA, STAR_SUVARNA, COLORS_KANNADA
from plugins.cbb import DATEDAY
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from datetime import datetime, timedelta
from helper_func import encode
from pyshorteners import Shortener
import string
import re
import time
import pytz

@Client.on_message(filters.private & filters.command(["date"]))
async def date(bot, message):
    dat = await message.reply_text("Select Date.........",quote=True,reply_markup=InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Yesterday",callback_data='ystdy'), 
        			InlineKeyboardButton("Today",callback_data = 'tdy'), 
        			InlineKeyboardButton("Tommorow",callback_data='tmr') ]]))

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.text & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    dateexc = datetime.now().strftime("%d")
    media = message.video or message.document
    filname= media.file_name.split("S0")[0]#[1][2]etc
    botfsno= hk = re.findall("S0.+E\d+", media.file_name)
    if int(dateexc) % 2 != 0:
        if filname in media.file_name:
            # chtid=int(ODD[filname][3])
            pic=ODD[filname][0]
            SL_URL=ODD[filname][1]
            SL_API=ODD[filname][2]
            bot_msg = await message.reply_text("Please Wait...!", quote = True)
            await asyncio.sleep(2)
            e_pic = await message.reply_photo(photo=pic, caption=f"....")
            await asyncio.sleep(2)
    elif int(dateexc) % 2 == 0:
        if filname in media.file_name:
            # chtid=int(EVEN[filname][3])
            pic=EVEN[filname][0]
            SL_URL=EVEN[filname][1]
            SL_API=EVEN[filname][2] 
            bot_msg = await message.reply_text("Please Wait...!", quote = True)
            await asyncio.sleep(2)
            e_pic = await message.reply_photo(photo=pic, caption=f"....")
            await asyncio.sleep(2)
    else:
        reply_text = await message.reply_text("❌Don't send me messages directly I'm only for serials!")
        
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    
    Slink = await get_short(SL_URL, SL_API, Tlink)
    await bot_msg.edit(BOTEFITMSG.format(filname, botfsno[0], Tlink, Slink, DATEDAY[0]))
    await e_pic.edit(FOMET.format(DATEDAY[-1], Slink, Slink))

    india = pytz.timezone("Asia/Kolkata")
    td = datetime.now(india)
    FILES_NAME = filname.split("S0")[0]
    tr = datetime.now(india) + timedelta(1)
    if DATEDAY[-1] == str(td.strftime("%d - %m - %Y")):
        TDSTAR_SUVARNA=dict()
        TDCOLORS_KANNADA=dict()
        TDZEE_KANNADA=dict()
        if FILES_NAME in STAR_SUVARNA:
            TDSTAR_SUVARNA[FILES_NAME]=Slink
        if FILES_NAME in COLORS_KANNADA:
            TDCOLORS_KANNADA[FILES_NAME]=Slink
        if FILES_NAME in ZEE_KANNADA:
            TDZEE_KANNADA[FILES_NAME]=Slink
        else:
            pass
    elif DATEDAY[-1] == str(tr.strftime("%d - %m - %Y")):
        TRSTAR_SUVARNA=dict()
        TRCOLORS_KANNADA=dict()
        TRZEE_KANNADA=dict()
        if FILES_NAME in STAR_SUVARNA:
            TRSTAR_SUVARNA[FILES_NAME]=Slink
        if FILES_NAME in COLORS_KANNADA:
            TRCOLORS_KANNADA[FILES_NAME]=Slink
        if FILES_NAME in ZEE_KANNADA:
            TRZEE_KANNADA[FILES_NAME]=Slink
        else:
            pass
    else:
        pass

    t = datetime.now(india)
    TIME_DAY = t.strftime('%H:%M %p')
    if TIME_DAY == "16:25 PM":
        if len(TDSTAR_SUVARNA) and len(TDCOLORS_KANNADA) and len(TDZEE_KANNADA) > 0:
            for KEY in TDSTAR_SUVARNA:
                txt_star = ''
                txt_star += f"{KEY}\n{TDSTAR_SUVARNA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_star)
            for KEY in TDCOLORS_KANNADA:
                txt_color = ''
                txt_color += f"{KEY}\n{TDCOLORS_KANNADA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_color)
            for KEY in TDZEE_KANNADA:
                txt_zee = ''
                txt_zee += f"{KEY}\n{TDZEE_KANNADA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_zee)
            TDSTAR_SUVARNA.clear()
            TDCOLORS_KANNADA.clear()
            TDZEE_KANNADA.clear()
        else:
            pass
        if len(TRSTAR_SUVARNA) > 0:
            TDSTAR_SUVARNA.clear()
            TDSTAR_SUVARNA = TRSTAR_SUVARNA
            for KEY in TDSTAR_SUVARNA:
                txt_star = ''
                txt_star += f"{KEY}\n{TDSTAR_SUVARNA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_star)
            TDSTAR_SUVARNA.clear()
            TRSTAR_SUVARNA.clear()
        elif len(TRCOLORS_KANNADA) > 0:
            TDCOLORS_KANNADA.clear()
            TDCOLORS_KANNADA = TRCOLORS_KANNADA
            for KEY in TDCOLORS_KANNADA:
                txt_color = ''
                txt_color += f"{KEY}\n{TDCOLORS_KANNADA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_color)
            TDCOLORS_KANNADA.clear()
            TRCOLORS_KANNADA.clear()
        elif len(TRZEE_KANNADA) > 0:
            TDZEE_KANNADA.clear()
            TDZEE_KANNADA = TRZEE_KANNADA
            for KEY in TDZEE_KANNADA:
                txt_zee = ''
                txt_zee += f"{KEY}\n{TDZEE_KANNADA[KEY]}\n\n"
                
            await client.send_message(chat_id=message.chat.id, text = txt_zee)
            TDZEE_KANNADA.clear()
            TRZEE_KANNADA.clear()
        else:
            pass
            
            
    #here we delete the edited post from the bot after 5min
    time.sleep(300)
    await e_pic.delete()
    

async def get_short(SL_URL, SL_API, Tlink):
    # FireLinks shorten
    try:
        api_url = f"https://{SL_URL}/api"
        params = {'api': SL_API, 'url': Tlink}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
        return url
    except Exception as error:
        return error
    
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
