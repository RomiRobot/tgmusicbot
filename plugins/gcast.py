# 𝑪𝒐𝒑𝒚𝒓𝒊𝒈𝒉𝒕 (C) 2022 𝑩𝒚 @𝑨𝒅𝒊𝒕𝒚𝒂𝑯𝒂𝒍𝒅𝒆𝒓

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant
from modules.clientbot.clientbot import client as aditya
from modules.config import SUDO_USERS

@Client.on_message(filters.command(["gcast", "broadcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("**`Starting Broadcast...`**")
        if not message.reply_to_message:
            await wtf.edit("**Please Reply To A Message...**")
            return
        lmao = message.reply_to_message.text
        async for dialog in aditya.iter_dialogs():
            try:
                await aditya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"**Broadcasting...** \n\n**Sent To:** `{sent}` **Chats** \n** Failed To:** `{failed}` **Chats**")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await wtf.delete()
        await message.reply_text(f"**Gcast Successfully...**\n\n**Sent To:** `{sent}` **Chats**\n**Failed To:** `{failed}` **Chats**")
