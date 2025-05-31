import io
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from XyrenMusic import app

@app.on_message(filters.command("q", prefixes="/") & filters.reply)
async def quotify(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        await message.reply("Balas pesan yang ingin dijadikan kutipan.")
        return

    sender = reply.from_user.first_name if reply.from_user else "Pengguna"
    text = reply.text or reply.caption or "Tidak ada teks."

    # Gambar dasar
    img = Image.new("RGB", (800, 400), color=(40, 42, 54))
    draw = ImageDraw.Draw(img)

    # Pakai default font dari PIL
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()

    # Tulis nama dan isi pesan
    draw.text((30, 40), f"{sender}:", font=font_title, fill=(255, 255, 255))
    draw.text((30, 80), text, font=font_text, fill=(220, 220, 220))

    # Potong ke area teks
    img = img.crop(img.getbbox())

    # Simpan sebagai WebP untuk stiker
    output = io.BytesIO()
    img.save(output, format="WEBP")
    output.name = "quote.webp"
    output.seek(0)

    await message.reply_sticker(output)
