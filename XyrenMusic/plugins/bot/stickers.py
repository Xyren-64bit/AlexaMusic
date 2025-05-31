import os
import io
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message, MessageEntity
from XyrenMusic import app

def get_msg_entities(msg: Message):
    entities = []
    if not msg.entities:
        return entities

    for entity in msg.entities:
        entities.append(
            {
                "type": entity.type,
                "offset": entity.offset,
                "length": entity.length,
            }
        )
    return entities

def quotify(data):
    try:
        message = data[0]
        text = message["text"]
        user_name = message["from"]["name"]
        reply_text = ""
        if message.get("replyMessage"):
            reply = message["replyMessage"]
            reply_name = reply.get("name", "Unknown")
            reply_content = reply.get("text", "")
            reply_text = f"{reply_name} said: {reply_content}\n\n"

        final_text = reply_text + f"{user_name}:\n{text}"

        # Create image
        img = Image.new("RGB", (600, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()

        draw.text((10, 10), final_text, fill=(0, 0, 0), font=font)

        output_path = "quote.webp"
        img.save(output_path, "WEBP")

        return True, output_path
    except Exception as e:
        return False, str(e)

@app.on_message(filters.command("q") & filters.reply)
async def quote_the_msg(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a message to quote it.")
        return

    to_edit = await m.reply_text("Generating quote...")

    reply_message = {}
    if len(m.command) > 1 and m.command[1].lower() == "r":
        reply_msg = m.reply_to_message.reply_to_message
        if reply_msg and reply_msg.text:
            await to_edit.edit_text("Generating quote with reply to the message...")
            replied_name = reply_msg.from_user.first_name
            if reply_msg.from_user.last_name:
                replied_name += f" {reply_msg.from_user.last_name}"

            reply_message = {
                "chatId": reply_msg.from_user.id,
                "entities": get_msg_entities(reply_msg),
                "name": replied_name,
                "text": reply_msg.text,
            }

    user = m.reply_to_message.from_user
    name = user.first_name
    if user.last_name:
        name += f" {user.last_name}"

    emoji_status = None
    if hasattr(user, "emoji_status") and user.emoji_status:
        emoji_status = str(user.emoji_status.custom_emoji_id)

    msg_data = [
        {
            "entities": get_msg_entities(m.reply_to_message),
            "avatar": True,
            "from": {
                "id": user.id,
                "name": name,
                "emoji_status": emoji_status,
            },
            "text": m.reply_to_message.text,
            "replyMessage": reply_message,
        }
    ]

    status, path = quotify(msg_data)

    if not status:
        await to_edit.edit_text(path)
        return

    await m.reply_sticker(path)
    await to_edit.delete()
    os.remove(path)
