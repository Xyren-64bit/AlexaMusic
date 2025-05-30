# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


from pyrogram import filters

import config
from strings import get_command
from XyrenMusic import app
from XyrenMusic.misc import SUDOERS
from XyrenMusic.utils.database import autoend_off, autoend_on
from XyrenMusic.utils.decorators.language import language

# Commands
AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message):
    usage = "**ᴜsᴀɢᴇ:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "ғɪᴛᴜʀ ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ ᴀᴋᴛɪғ.\n\nᴀssɪsᴛᴀɴᴛ ᴀᴋᴀɴ ᴏᴛᴏᴍᴀᴛɪs ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ᴠɪᴅᴇᴏᴄʜᴀᴛ sᴇᴛᴇʟᴀʜ ʙᴇʙᴇʀᴀᴘᴀ ᴍᴇɴɪᴛ ᴋᴀʀᴇɴᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ʏᴀɴɢ ᴍᴇɴᴅᴇɴɢᴀʀ, ᴅɪᴋɪʀɪᴍ ᴅᴇɴɢᴀɴ ᴘᴇsᴀɴ ᴘᴇʀɪɴɢᴀᴛᴀɴ."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ dinonaktifkan.")
    else:
        await message.reply_text(usage)
