# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, adminlist
from strings import get_command
from XyrenMusic import app
from XyrenMusic.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from XyrenMusic.utils.decorators import AdminActual, language
from XyrenMusic.utils.formatters import int_to_alpha

# Command
AUTH_COMMAND = get_command("AUTH_COMMAND")
UNAUTH_COMMAND = get_command("UNAUTH_COMMAND")
AUTHUSERS_COMMAND = get_command("AUTHUSERS_COMMAND")


@app.on_message(filters.command(AUTH_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = len(_check)
        if count == 20:
            return await message.reply_text(_["auth_1"])
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            if get := adminlist.get(message.chat.id):
                if user.id not in get:
                    get.append(user.id)
            await save_authuser(message.chat.id, token, assis)
            return await message.reply_text(_["auth_2"])
        else:
            await message.reply_text(_["auth_3"])
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for _ in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(_["auth_1"])
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        if get := adminlist.get(message.chat.id):
            if user_id not in get:
                get.append(user_id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(_["auth_2"])
    else:
        await message.reply_text(_["auth_3"])


@app.on_message(filters.command(UNAUTH_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if get := adminlist.get(message.chat.id):
            if user.id in get:
                get.remove(user.id)
        if deleted:
            return await message.reply_text(_["auth_4"])
        else:
            return await message.reply_text(_["auth_5"])
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if get := adminlist.get(message.chat.id):
        if user_id in get:
            get.remove(user_id)
    if deleted:
        return await message.reply_text(_["auth_4"])
    else:
        return await message.reply_text(_["auth_5"])


@app.on_message(filters.command(AUTHUSERS_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def authusers(client, message: Message, _):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(_["setting_5"])
    j = 0
    mystic = await message.reply_text(_["auth_6"])
    text = _["auth_7"]
    for note in _playlist:
        _note = await get_authuser(message.chat.id, note)
        user_id = _note["auth_user_id"]
        admin_id = _note["admin_id"]
        admin_name = _note["admin_name"]
        try:
            user = await app.get_users(user_id)
            user = user.first_name
            j += 1
        except Exception:
            continue
        text += f"{j}➤ {user}[`{user_id}`]\n"
        text += f"   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
    await mystic.delete()
    await message.reply_text(text)
