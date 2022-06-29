# 𝐀𝐝𝐢𝐭𝐲𝐚 𝐇𝐚𝐥𝐝𝐞𝐫 // @𝑨𝒅𝒊𝒕𝒚𝒂𝑯𝒂𝒍𝒅𝒆𝒓
import os
import aiofiles
import aiohttp
import ffmpeg
import random
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import ASSISTANT_USERNAME, DURATION_LIMIT, que, OWNER_USERNAME, SUDO_USERS, SUPPORT_GROUP, UPDATES_CHANNEL, PROFILE_CHANNEL
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# 𝑰𝒏𝒕𝒆𝒓𝒏𝒂𝒍 𝑴𝒐𝒅𝒖𝒍𝒆𝒔
chat_id = None
useer = "NaN"

themes = [
    "bgreen",
    "blue",
    "colorfull",
    "dgreen",
    "hgreen",
    "lgreen",
    "lyellow",
    "orange",
    "pink",
    "purple",
    "rainbow",
    "red",
    "sky",
    "thumbnail",
    "yellow",
]

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# 𝑪𝒐𝒏𝒗𝒆𝒓𝒕 𝑺𝒆𝒄𝒐𝒏𝒅𝒔 𝑻𝒐 𝒎𝒎:𝒔𝒔
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# 𝑪𝒐𝒏𝒗𝒆𝒓𝒕 𝒉𝒉:𝒎𝒎:𝒔𝒔 𝑻𝒐 𝑺𝒆𝒄𝒐𝒏𝒅𝒔
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# 𝑪𝒉𝒂𝒏𝒈𝒆 𝑻𝒉𝒖𝒎𝒃𝒏𝒂𝒊𝒍 𝑺𝒊𝒛𝒆
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))

# 𝑮𝒆𝒏𝒆𝒓𝒂𝒕𝒆 𝑻𝒉𝒖𝒎𝒃𝒏𝒂𝒊𝒍
async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    theme = random.choice(themes)
    image1 = Image.open("./background.png")
    image2 = Image.open(f"resource/{theme}.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: Aditya Halder (@AdityaHalder)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", ".play", "!play", "play", "@", "#", "$"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    await message.delete()
    lel = await message.reply("**•🔎  Sᴇᴀʀᴄʜɪɴɢ •...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Romi_Robot"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**At First Make Me Admin ...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**I Am Ready To Play...**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**Please Manually Add [Assistant](t.me/{ASSISTANT_USERNAME}) In This Group Or Cantact To [Bot Owner](https://t.me/{OWNER_USERNAME}) **")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**Please Add Manually [Assistant](t.me/{ASSISTANT_USERNAME}) In This Group Or Cantact To [Bot Owner(https://t.me/{OWNER_USERNAME}) **")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**• Pʟᴀʏ Mᴜsɪᴄ Lᴇss\nTʜᴀɴ {DURATION_LIMIT} Mɪɴᴜᴛᴇ • ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/64dcf7da559b7021edbc3.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="• Oᴡɴᴇʀ •",
                            url=f"https://t.me/{OWNER_USERNAME}")
               ],
               [
                    InlineKeyboardButton(
                            text="• Uᴘᴅᴀᴛᴇs •",
                            url=f"{UPDATES_CHANNEL}"),
                            
                    InlineKeyboardButton(
                            text="• Sᴜᴘᴘᴏʀᴛ •",
                            url=f"{SUPPORT_GROUP}")
               ],
               [
                        InlineKeyboardButton(
                            text="• Aʙᴏᴜᴛ •",
                            url=f"{PROFILE_CHANNEL}")
                   
                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="• Oᴡɴᴇʀ •",
                            url=f"https://t.me/{OWNER_USERNAME}")
               ],
               [
                    InlineKeyboardButton(
                            text="• Uᴘᴅᴀᴛᴇs •",
                            url=f"{UPDATES_CHANNEL}"),
                            
                    InlineKeyboardButton(
                            text="• Sᴜᴘᴘᴏʀᴛ •",
                            url=f"{SUPPORT_GROUP}")
               ],
               [
                        InlineKeyboardButton(
                            text="• Aʙᴏᴜᴛ •",
                            url=f"{PROFILE_CHANNEL}")
                   
                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/64dcf7da559b7021edbc3.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="• Oᴡɴᴇʀ •",
                            url=f"https://t.me/{OWNER_USERNAME}")
               ],
               [
                    InlineKeyboardButton(
                            text="• Uᴘᴅᴀᴛᴇs •",
                            url=f"{UPDATES_CHANNEL}"),
                            
                    InlineKeyboardButton(
                            text="• Sᴜᴘᴘᴏʀᴛ •",
                            url=f"{SUPPORT_GROUP}")
               ],
               [
                        InlineKeyboardButton(
                            text="• Aʙᴏᴜᴛ •",
                            url=f"{PROFILE_CHANNEL}")
                   
                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**Play Music Less \n Than {DURATION_LIMIT} Minute ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**Give Music Name \n To Play Song...**"
            )
        await lel.edit("**🔄 Processing...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**Music Not Found! \n Try Another...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="• Oᴡɴᴇʀ •",
                            url=f"https://t.me/{OWNER_USERNAME}")
               ],
               [
                    InlineKeyboardButton(
                            text="• Uᴘᴅᴀᴛᴇs •",
                            url=f"{UPDATES_CHANNEL}"),
                            
                    InlineKeyboardButton(
                            text="• Sᴜᴘᴘᴏʀᴛ •",
                            url=f"{SUPPORT_GROUP}")
               ],
               [
                        InlineKeyboardButton(
                            text="• Aʙᴏᴜᴛ •",
                            url=f"{PROFILE_CHANNEL}")
                   
                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**Play Music Less \n Than {DURATION_LIMIT} Minute...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**Your Song Queued! \n At Position » `{}` ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**Romi X Robot Now \n Playing OP...**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["pause", ".pause", "/pause", "!pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("**▶️ Paused...**"
    )


@Client.on_message(commandpro(["resume", ".resume", "/resume", "!resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("**⏸ Rᴇsᴜᴍᴇᴅ • ...**"
    )



@Client.on_message(commandpro(["skip", ".skip", "/skip", "!skip"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**Romi X Robot Nothing \n Playing...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await message.reply_text("**Queue Empty, Leaving VC...**") 
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            await message.reply_text("**⏩ Skipped...**") 
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )



@Client.on_message(commandpro(["end", "/end", "!end", ".end", "stop", "/stop", ".stop", "stop", "x"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    await message.delete()
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("**❌ Stopped...**"
    )


@Client.on_message(commandpro(["reload", ".reload", "/reload", "!reload", "/admincache"]))
@errors
@authorized_users_only
async def update_admin(client, message):
    global a
    await message.delete()
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    a[message.chat.id] = new_admins
    await message.reply_text("**Reloaded...**")
