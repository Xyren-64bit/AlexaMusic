import io
from io import BytesIO
from pyrogram import filters, Client
from pyrogram.types import Message
from XyrenMusic import app
from httpx import AsyncClient

fetch = AsyncClient()

class QuotlyException(Exception):
    pass


async def get_message_sender_id(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return 1
        elif ctx.forward_from:
            return ctx.forward_from.id
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.id
        else:
            return 1
    elif ctx.from_user:
        return ctx.from_user.id
    elif ctx.sender_chat:
        return ctx.sender_chat.id
    else:
        return 1


async def get_message_sender_name(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return ctx.forward_sender_name
        elif ctx.forward_from:
            return (
                f"{ctx.forward_from.first_name} {ctx.forward_from.last_name}"
                if ctx.forward_from.last_name
                else ctx.forward_from.first_name
            )
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.title
        else:
            return ""
    elif ctx.from_user:
        if ctx.from_user.last_name:
            return f"{ctx.from_user.first_name} {ctx.from_user.last_name}"
        else:
            return ctx.from_user.first_name
    elif ctx.sender_chat:
        return ctx.sender_chat.title
    else:
        return ""


async def get_custom_emoji(ctx: Message):
    if ctx.forward_date:
        return (
            ""
            if ctx.forward_sender_name
            or not ctx.forward_from
            and ctx.forward_from_chat
            or not ctx.forward_from
            else ctx.forward_from.emoji_status.custom_emoji_id
        )
    return ctx.from_user.emoji_status.custom_emoji_id if ctx.from_user else ""


async def get_message_sender_username(ctx: Message):
    if ctx.forward_date:
        if (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            and ctx.forward_from_chat.username
        ):
            return ctx.forward_from_chat.username
        elif (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            or ctx.forward_sender_name
            or not ctx.forward_from
        ):
            return ""
        else:
            return ctx.forward_from.username or ""
    elif ctx.from_user and ctx.from_user.username:
        return ctx.from_user.username
    elif (
        ctx.from_user
        or ctx.sender_chat
        and not ctx.sender_chat.username
        or not ctx.sender_chat
    ):
        return ""
    else:
        return ctx.sender_chat.username


async def get_message_sender_photo(ctx: Message):
    if ctx.forward_date:
        if (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            and ctx.forward_from_chat.photo
        ):
            return {
                "small_file_id": ctx.forward_from_chat.photo.small_file_id,
                "small_photo_unique_id": ctx.forward_from_chat.photo.small_photo_unique_id,
                "big_file_id": ctx.forward_from_chat.photo.big_file_id,
                "big_photo_unique_id": ctx.forward_from_chat.photo.big_photo_unique_id,
            }
        elif (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            or ctx.forward_sender_name
            or not ctx.forward_from
        ):
            return ""
        else:
            return (
                {
                    "small_file_id": ctx.forward_from.photo.small_file_id,
                    "small_photo_unique_id": ctx.forward_from.photo.small_photo_unique_id,
                    "big_file_id": ctx.forward_from.photo.big_file_id,
                    "big_photo_unique_id": ctx.forward_from.photo.big_photo_unique_id,
                }
                if ctx.forward_from.photo
                else ""
            )

    elif ctx.from_user and ctx.from_user.photo:
        return {
            "small_file_id": ctx.from_user.photo.small_file_id,
            "small_photo_unique_id": ctx.from_user.photo.small_photo_unique_id,
            "big_file_id": ctx.from_user.photo.big_file_id,
            "big_photo_unique_id": ctx.from_user.photo.big_photo_unique_id,
        }
    elif (
        ctx.from_user
        or ctx.sender_chat
        and not ctx.sender_chat.photo
        or not ctx.sender_chat
    ):
        return ""
    else:
        return {
            "small_file_id": ctx.sender_chat.photo.small_file_id,
            "small_photo_unique_id": ctx.sender_chat.photo.small_photo_unique_id,
            "big_file_id": ctx.sender_chat.photo.big_file_id,
            "big_photo_unique_id": ctx.sender_chat.photo.big_photo_unique_id,
        }


async def get_text_or_caption(ctx: Message):
    return ctx.text or ctx.caption or ""


async def pyrogram_to_quotly(messages, is_reply):
    if not isinstance(messages, list):
        messages = [messages]
    payload = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "messages": [],
    }

    for message in messages:
        msg_dict = {
            "chatId": await get_message_sender_id(message),
            "text": await get_text_or_caption(message),
            "avatar": True,
            "from": {
                "id": await get_message_sender_id(message),
                "name": await get_message_sender_name(message),
                "username": await get_message_sender_username(message),
                "type": message.chat.type.name.lower(),
                "photo": await get_message_sender_photo(message),
            },
            "entities": [],
            "replyMessage": {},
        }

        if message.entities:
            msg_dict["entities"] = [
                {"type": e.type.name.lower(), "offset": e.offset, "length": e.length}
                for e in message.entities
            ]
        elif message.caption_entities:
            msg_dict["entities"] = [
                {"type": e.type.name.lower(), "offset": e.offset, "length": e.length}
                for e in message.caption_entities
            ]

        if message.reply_to_message and is_reply:
            msg_dict["replyMessage"] = {
                "name": await get_message_sender_name(message.reply_to_message),
                "text": await get_text_or_caption(message.reply_to_message),
                "chatId": await get_message_sender_id(message.reply_to_message),
            }

        payload["messages"].append(msg_dict)

    r = await fetch.post("https://bot.lyo.su/quote/generate.png", json=payload)
    if r.status_code == 200:
        return r.content
    else:
        raise QuotlyException(r.json())


def isArgInt(txt) -> list:
    try:
        count = int(txt)
        return [True, count]
    except ValueError:
        return [False, 0]


@app.on_message(filters.command(["q", "qr"]) & filters.reply)
async def msg_quotly_cmd(self: Client, ctx: Message):
    is_reply = ctx.command[0].endswith("r")

    if len(ctx.text.split()) > 1:
        check_arg = isArgInt(ctx.command[1])
        if check_arg[0]:
            if check_arg[1] < 2 or check_arg[1] > 10:
                return await ctx.reply("Rentang hanya 2–10.")
            try:
                messages = [
                    m for m in await self.get_messages(
                        ctx.chat.id,
                        list(range(
                            ctx.reply_to_message.id,
                            ctx.reply_to_message.id + check_arg[1]
                        )),
                        replies=-1,
                    ) if not m.empty and not m.media
                ]
                quotly_img = await pyrogram_to_quotly(messages, is_reply=is_reply)
                output = BytesIO(quotly_img)
                output.name = "quote.webp"
                output.seek(0)
                return await ctx.reply_sticker(output)
            except Exception:
                return await ctx.reply("❌ Gagal membuat stiker.")
    try:
        msg = await self.get_messages(ctx.chat.id, ctx.reply_to_message.id, replies=-1)
        quotly_img = await pyrogram_to_quotly([msg], is_reply=is_reply)
        output = BytesIO(quotly_img)
        output.name = "quote.webp"
        output.seek(0)
        return await ctx.reply_sticker(output)
    except Exception as e:
        return await ctx.reply(f"ERROR: {e}")
