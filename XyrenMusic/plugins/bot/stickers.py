import io
from pyrogram import filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
from XyrenMusic import app


def create_quotly_style_sticker(text: str, username: str) -> io.BytesIO:
    max_width = 512
    padding = 40
    bg_color = (47, 35, 64)         # Warna bubble gelap
    username_color = (255, 153, 0)  # Orange
    text_color = (255, 255, 255)

    # Gunakan font sistem atau default
    try:
        font = ImageFont.truetype("arial.ttf", 36)
        username_font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
        username_font = ImageFont.load_default()

    # Gambar sementara untuk menghitung ukuran
    temp = Image.new("RGB", (max_width, 1000))
    draw = ImageDraw.Draw(temp)

    def wrap(text, font, max_width):
        words = text.split()
        lines, line = [], ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width - 2 * padding:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    lines = wrap(text, font, max_width)
    line_height = font.getbbox("A")[3]
    username_height = username_font.getbbox("A")[3]
    total_height = padding + username_height + len(lines) * line_height + padding

    # Gambar akhir
    img = Image.new("RGB", (max_width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    draw.text((padding, padding), username, font=username_font, fill=username_color)

    y = padding + username_height + 10
    for line in lines:
        draw.text((padding, y), line, font=font, fill=text_color)
        y += line_height

    # Resize ke 512x512
    img = img.resize((512, 512))
    output = io.BytesIO()
    img.save(output, format="WEBP")
    output.name = "sticker.webp"
    output.seek(0)
    return output


@app.on_message(filters.command("q") & filters.reply)
async def quotly_command(_, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("❌ Balas pesan teks untuk dijadikan stiker.")

    username = (
        reply.from_user.username or reply.from_user.first_name
    )
    text = reply.text

    await message.reply("🎨 Membuat stiker...")

    try:
        sticker = create_quotly_style_sticker(text, username)
        await app.send_sticker(
            chat_id=message.chat.id,
            sticker=sticker,
            reply_to_message_id=message.id
        )
    except Exception as e:
        await message.reply(f"⚠️ Gagal membuat stiker: {e}")
