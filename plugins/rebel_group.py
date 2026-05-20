from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, ChatPrivileges

# 1. أمر الحظر (طرد نهائي)
@Client.on_message(filters.command("حظر") & filters.group & filters.reply)
async def ban_user(client, message):
    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply_text(f"**- أبشر، تم حظر {message.reply_to_message.from_user.first_name} طيران! ✈️**")

# 2. أمر الطرد (يطرده ويقدر يرجع)
@Client.on_message(filters.command("طرد") & filters.group & filters.reply)
async def kick_user(client, message):
    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply_text(f"**- تم طرد {message.reply_to_message.from_user.first_name} من المجموعة 🚷**")

# 3. أمر الكتم (يمنعه من الكتابة فقط)
@Client.on_message(filters.command("كتم") & filters.group & filters.reply)
async def mute_user(client, message):
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(can_send_messages=False)
    )
    await message.reply_text(f"**- تم كتم {message.reply_to_message.from_user.first_name}.. خليه يسكت! 🤐**")

# 4. أمر التقييد (يمنعه من كل شيء: وسائط، روابط، رسائل)
@Client.on_message(filters.command("تقييد") & filters.group & filters.reply)
async def restrict_user(client, message):
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
    )
    await message.reply_text(f"**- تم تقييد {message.reply_to_message.from_user.first_name} بنجاح 🔐**")

# 5. أمر إلغاء الكتم/التقييد
@Client.on_message(filters.command(["الغاء الكتم", "الغاء التقييد"]) & filters.group & filters.reply)
async def unmute_user(client, message):
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )
    await message.reply_text(f"**- تم فك القيود عن {message.reply_to_message.from_user.first_name} ✨**")

# 6. أمر رفع مدير (ترقية لمشرف)
@Client.on_message(filters.command("رفع مدير") & filters.group & filters.reply)
async def promote_user(client, message):
    await client.promote_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True
        )
    )
    await message.reply_text(f"**- صار {message.reply_to_message.from_user.mention} مدير الآن! 🎖️**")
