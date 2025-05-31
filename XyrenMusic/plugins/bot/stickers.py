import io
from pyrogram import filters
from pyrogram.types import Message, InputSticker, InputMediaSticker
from PIL import Image, ImageDraw, ImageFont
from XyrenMusic import app


def create_quote_sticker(text: str, username: str) -> io.BytesIO:
    # Ukuran dasar stiker
    width, height = 512, 512
    background_color = (255, 255, 255, 0)  # Transparan
    text_color = (0, 0, 0)

    # Membuat gambar kosong
    img = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Memuat font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        username_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        username_font = ImageFont.load_default()

    # Menulis nama pengguna
    draw.text((20, 20), f"@{username}:", font=username_font, fill=(80, 80, 80))

    # Menulis teks
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if draw.textlength(line + word, font=font) < 460:
            line += f"{word} "
        else:
            lines.append(line)
            line = f"{word} "
    lines.append(line)

    y = 60
    for line in lines:
        draw.text((20, y), line.strip(), font=font, fill=text_color)
        y += 35

    # Simpan ke dalam buffer
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.name = "quote.png"
    output.seek(0)
    return output


@app.on_message(filters.command("q") & filters.reply)
async def make_quote_sticker(_, message: Message):
    reply = message.reply_to_message

    if not reply.text:
        return await message.reply("❌ Balas pesan teks untuk dijadikan stiker.")

    username = (
        reply.from_user.username if reply.from_user.username else reply.from_user.first_name
    )
    text = reply.text

    await message.reply("🛠️ Membuat stiker...")

    try:
        sticker_bytes = create_quote_sticker(text, username)
        await app.send_sticker(
            chat_id=message.chat.id,
            sticker=sticker_bytes,
            reply_to_message_id=message.id
        )
    except Exception as e:
        await message.reply(f"⚠️ Gagal membuat stiker: {e}")
