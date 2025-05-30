from XyrenMusic import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions, ChatMemberUpdated

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [
    " **➠ ʜᴇʏ ʙᴇʙ, ʟᴜ ᴅɪ ᴍᴀɴᴀ 🤗** ",
    " **➠ ᴏʏ, ᴛɪᴅᴜʀ ᴍᴜʟᴜ ʟᴜ, ʏᴜᴋ ᴏɴʟɪɴᴇ 😊** ",
    " **➠ ɢᴀs ᴋᴇ ᴠᴄ, ɴɢᴏʙʀᴏʟ ʏᴜᴋ 😃** ",
    " **➠ ᴜᴅᴀʜ ᴍᴀᴋᴀɴ ʙᴇʟᴜᴍ ɴɪʜ..?? 🥲** ",
    " **➠ ɢɪᴍᴀɴᴀ ᴋᴀʙᴀʀ ᴏʀᴀɴɢ ʀᴜᴍᴀʜ 🥺** ",
    " **➠ ɢᴜᴇ ᴋᴀɴɢᴇɴ ʙᴀɴɢᴇᴛ sᴀᴍᴀ ʟᴜ 🤭** ",
    " **➠ ᴏʏᴇ, ᴘɪʀᴀ ᴋᴀʙᴀʀɴʏᴀ..?? 🤨** ",
    " **➠ ʙɪsᴀɪɴ ᴊᴏᴅᴏʜɪɴ ɢᴜᴇ ɴɢɢᴀ..? 🙂** ",
    " **➠ ɴᴀᴍᴀ ʟᴜ sɪᴀᴘᴀ sɪʜ..?? 🥲** ",
    " **➠ ᴜᴅᴀʜ ᴍᴀᴋᴀɴ ʙᴇʟᴜᴍ..?? 😋** ",
    " **➠ ᴋɪᴅɴᴀᴘ ɢᴜᴇ ᴋᴇ ɢʀᴏᴜᴘ ʟᴜ ᴅᴏɴɢ 😍** ",
    " **➠ ᴘᴀsᴀɴɢᴀɴ ʟᴜ ʟᴀɢɪ ɴʏᴀʀɪɴ, ʙᴜʀᴜᴀɴ ᴏɴʟɪɴᴇ 😅** ",
    " **➠ ᴍᴀᴜ ᴛᴇᴍᴀɴᴀɴ ɢᴀ ᴅᴇɴɢᴀɴ ɢᴜᴇ..?? 🤔** ",
    " **➠ ᴛɪᴅᴜʀ ᴏʀᴀɴɢɴʏᴀ ʏᴀ.. 🙄** ",
    " **➠ ᴘʟᴀʏ ʟᴀɢᴜ ᴅᴏɴɢ, ᴘʟss 😕** ",
    " **➠ ᴅᴀʀɪ ᴍᴀɴᴀ ʟᴜ..?? 🙃** ",
    " **➠ ʜᴀʟᴏ ʏᴀ ɴᴀᴍᴀsᴛᴇ 😛** ",
    " **➠ ʜᴀʟᴏ ʙᴀʙʏ, ɢᴍɴ ɴɪʜ..? 🤔** ",
    " **➠ ᴛᴀᴜ ɢᴀ sɪᴀᴘᴀ ᴏᴡɴᴇʀ ɢᴜᴇ..? ☺️** ",
    " **➠ ʏᴜᴋ ᴍᴀɪɴ ɢᴀᴍᴇ ʏᴜᴋ 🤗** ",
    " **➠ ᴄɪᴛᴀ, ɢᴍɴ ᴋᴀʙᴀʀɴʏᴀ 😇** ",
    " **➠ ᴍᴀᴍᴀ ʟᴜ ʟᴀɢɪ ɴɢᴀᴘᴀɪɴ 🤭** ",
    " **➠ ᴋᴏᴋ ɢᴀ ᴍᴀᴜ ɴɢᴏʙʀᴏʟ sᴀᴍᴀ ɢᴜᴇ 🥺** ",
    " **➠ ᴏʏᴇ ᴘᴀɢᴀʟ, ʙᴜʀᴜᴀɴ ᴏɴʟɪɴᴇ 😶** ",
    " **➠ ʜᴀʀɪ ɪɴɪ ʟɪʙᴜʀ ɢᴀ ᴅɪ sᴋᴜʟ..? 🤔** ",
    " **➠ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ʙʀᴏ 😜** ",
    " **➠ ᴇʜ ᴀᴅᴀ ᴛᴜɢᴀs ɴɪʜ, ᴛᴏʟᴏɴɢɪɴ ᴅɪᴋɪᴛ 🙂** ",
    " **➠ ᴘʟᴀʏ ʟᴀɢᴜ ʏᴀɴɢ ᴇɴᴀᴋ ᴅɪᴋɪᴛ ᴅᴏɴɢ 😪** ",
    " **➠ sᴇɴᴀɴɢ ᴋᴇɴᴀʟ ʟᴜ ☺** ",
    ...
]

VC_TAG = [
    "**➠ ᴏʏ ɢᴀʙᴜɴɢ ᴋᴇ ᴠᴄ ᴅᴏɴɢ 😒**",
    "**➠ ᴄᴇᴘᴇᴛᴀɴ ᴍᴀsᴜᴋ ᴋᴇ ᴠᴄ, ᴘᴇɴᴛɪɴɢ ɪɴɪ 😐**",
    "**➠ ʙᴇʙ, ʏᴜᴋ ᴍᴀsᴜᴋ ᴠᴄ ᴄᴇᴘᴇᴛᴀɴ 🙄**",
    "**➠ ᴅɪᴀᴍ-ᴅɪᴀᴍ ɢᴀʙᴜɴɢ ᴋᴇ ᴠᴄ 🤫**",
    "**➠ ɢᴜᴇ ɴɢᴇɴᴛɪ ᴅɪ ᴠᴄ, ᴛᴜɴɢɢᴜɪɴ ʟᴏ 🥺**",
    "**➠ ᴍᴀsᴜᴋ ᴋᴇ ᴠᴄ, ᴋɪᴛᴀ ɴɢᴏʙʀᴏʟ ʏᴜᴋ ☺️**",
    "**➠ ʙᴀʙᴜ, ᴄᴏʙᴀ ᴅᴇʜ ᴍᴀsᴜᴋ ᴠᴄ ɴʏᴇᴛ 🤨**",
    "**➠ ᴇʜ, ᴅɪ ᴠᴄ ɪᴛᴜ ᴏʀᴀɴɢ ʀᴜssɪᴀ ɴɢᴀᴘᴀɪɴ ʏᴀ 😮‍💨**",
    "**➠ ᴍᴀsᴜᴋ ᴋᴇ ᴠᴄ ʙɪᴀʀ ᴅɪʜɪᴀs ᴡᴀʀɴᴀ-ᴡᴀʀɴɪ 🤭**",
    "**➠ sᴏʀʀʏ ʙᴇʙ, ʏᴜᴋ ᴅᴏɴɢ ᴍᴀsᴜᴋ ᴠᴄ 😢**",
    "**➠ ᴍᴀsᴜᴋ ᴠᴄ ᴅɪᴋɪᴛ ᴀᴊᴀ, ʀᴀsᴀɴʏ ᴘᴇɴɢᴇɴ 😮**",
    "**➠ ᴄᴇᴋ ᴅɪ ᴠᴄ, ʟᴀɢᴜ ᴀᴘᴀ ᴛᴜʜ ʏᴀɴɢ ᴅɪᴘᴜᴛᴀʀ 💫**",
    "**➠ ɢᴀʙᴜɴɢ ᴋᴇ ᴠᴄ, ɢᴀ ʀᴜɢɪ ᴋᴏᴋ, ʟᴀɢɪ sᴇʀᴜ 😇**",
    "**➠ ᴅᴇᴀʀ, ʏᴜᴋ ᴠᴄ ɴᴀ, ᴀᴅᴀ ʟɪᴠᴇ sʜᴏᴡ ɴɪ 😵‍💫**",
    "**➠ ᴏᴡɴᴇʀ ᴋᴀᴍᴜ ɴɢɪɴɢɪɴ ᴋᴇ ᴠᴄ ᴅᴏɴɢ 😕**",
    "**➠ ʜᴇʏ ɢᴇᴍᴇs, ʏᴜᴋ ᴋᴇ ᴠᴄ sᴇᴋᴀʟɪɪɪ... 🌟**",
    "**➠ ᴍᴀᴜ ᴍᴀsᴜᴋ ᴋᴇ ᴠᴄ ɢᴀ sɪʜ... ✨**",
    "**➠ ᴍᴀsᴜᴋ ᴋᴇ ᴠᴄ ᴀᴛᴀᴜ ɢᴜᴇ ᴊᴇᴍᴘᴜᴛ ᴅᴀʀɪ ʀᴜᴍᴀʜ 🌝**",
    "**➠ ʙᴇʙ, ᴋᴀᴘᴀɴ ɴɪ ᴍᴀᴜ ᴍᴀsᴜᴋ ᴠᴄ 💯**",
]

user_update_cache = {}

# Batas waktu buat spam per user (detik)
THROTTLE_TIME = 60  # 1 menit

# Kalau cache udah penuh, bersihin
MAX_CACHE_SIZE = 500

def cleanup_cache():
    global user_update_cache
    if len(user_update_cache) >= MAX_CACHE_SIZE:
        now = time.time()
        user_update_cache = {
            uid: ts for uid, ts in user_update_cache.items()
            if now - ts < THROTTLE_TIME
        }

@app.on_chat_member_updated()
async def sang_mata_listener(client, update: ChatMemberUpdated):
    # Amankan kalau salah satu objek None
    old_member = update.old_chat_member
    new_member = update.new_chat_member
    chat_id = update.chat.id

    if not old_member or not new_member or not old_member.user or not new_member.user:
        return

    old_user = old_member.user
    new_user = new_member.user
    user_id = new_user.id
    now = time.time()

    # Bersihin cache kalau udah penuh
    cleanup_cache()

    # Cek throttle per user (biar nggak spam)
    if user_id in user_update_cache and now - user_update_cache[user_id] < THROTTLE_TIME:
        return

    user_update_cache[user_id] = now

    # Ambil nama dan bandingkan
    old_name = f"{old_user.first_name or ''} {old_user.last_name or ''}".strip()
    new_name = f"{new_user.first_name or ''} {new_user.last_name or ''}".strip()

    changes = []

    if old_name != new_name:
        changes.append(f"📝 **Nama lo berubah nih:**\n`{old_name}` ➜ `{new_name}`")

    if old_user.username != new_user.username:
        changes.append(
            f"📛 **Username ganti coy:**\n@{old_user.username or 'Gak ada'} ➜ @{new_user.username or 'Gak ada'}"
        )

    if changes:
        await asyncio.sleep(1)  # jeda biar server gak ngos-ngosan
        try:
            await client.send_message(
                chat_id,
                "\n".join(changes) + f"\n\n🕵️ *Sang Mata nemu perubahan dari* [{new_user.first_name}](tg://user?id={user_id}) 😎"
            )
        except Exception as e:
            print(f"⚠️ Gagal ngirim info Sang Mata: {e}")



@app.on_message(filters.command(["tagall", "tagmember" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ woy! Lu bukan admin gausah sok asik buat tagall")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall sᴇʟᴀᴍᴀᴛ ᴘᴀɢɪɪɪ ᴛʏᴘᴇ ɴʏᴀ ᴋᴀʏᴀ ɢɪɴɪ / ʙᴀʟᴀs ᴀᴊᴀ ᴘᴇsᴀɴ ɴʏᴀ ᴋᴀʟᴏ ɴᴛᴀʀ ʙᴏᴛ ɴᴀɴᴅᴀɪɴ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("/tagall sᴇʟᴀᴍᴀᴛ ᴘᴀɢɪɪɪ ᴛʏᴘᴇ ɴʏᴀ ᴋᴀʏᴀ ɢɪɴɪ / ʙᴀʟᴀs ᴀᴊᴀ ᴘᴇsᴀɴ ɴʏᴀ ᴋᴀʟᴏ ɴᴛᴀʀ ʙᴏᴛ ɴᴀɴᴅᴀɪɴ...")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["vctag"], prefixes=["/", "@", "#"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ Perintah ini hanya untuk group bang")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ woy! Lu bukan admin gausah sok asik buat tag member ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟɪss ʜᴇɴᴛɪɪɴ ᴅᴜʟᴜ ᴘʀᴏsᴇs ᴍᴇɴᴛɪᴏɴ ɴʏᴀ......")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["cancel", "tagstop", "vcstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ sᴇᴋᴀʀᴀɴɢ ɢᴜᴇ ɢᴀ ɴɢᴛᴀɢ ᴀᴘᴀ-ᴀᴘᴀ ʟᴏʜ ʙᴇʙ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ woy! Lu bukan admin gausah sok asik buat tag member .")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ proses tag berhenti ๏")