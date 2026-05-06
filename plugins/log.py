import asyncio
import os
from telethon import events, functions, types
# الربط بقلب السورس
from __main__ import client

# إعدادات المملكة
GROUP_NAME = "سجل رسائل المتمرد التقني 🦅🛡️"
STORAGE_CACHE = {"id": None}

async def get_log_group():
    """دالة ذكية للبحث عن الجروب أو إنشائه"""
    if STORAGE_CACHE["id"]:
        return STORAGE_CACHE["id"]

    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name == GROUP_NAME:
            STORAGE_CACHE["id"] = dialog.id
            return dialog.id
    return None

# 1. أمر إنشاء المملكة (تخزين جديد)
@client.on(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_fakhama_log(event):
    await event.edit("**- جـاري تـأسيس مـملكة الـتخزين الـفخمة... 🏗️**")
    try:
        existing_group = await get_log_group()
        if existing_group:
            return await event.edit(f"**✅ الـمملكة مـوجودة بـالفعل!\n🆔 الآيـدي:** `{existing_group}`")

        # إنشاء الجروب الجديد
        result = await client(functions.channels.CreateChannelRequest(
            title=GROUP_NAME,
            about="مستودع بيانات المتمرد التقني - حفظ الرسائل المهمة.",
            megagroup=True
        ))
        new_id = result.chats[0].id
        STORAGE_CACHE["id"] = new_id
        await event.edit(f"**✅ تـم إنـشاء مـملكة الـتخزين بـنجاح!**\n**الآن أي رسـالة سـيتم حـفظها هـنا.**")
    except Exception as e:
        await event.edit(f"**❌ حـدث خـطأ أثـناء الإنـشاء: {e}**")

# 2. نظام حفظ الرسائل (تحويل الرسائل المهمة للمملكة)
@client.on(events.NewMessage(incoming=True))
async def logger_task(event):
    # حفظ رسائل الخاص فقط (كمثال) لعدم امتلاء التخزين
    if event.is_private and not event.out:
        log_id = await get_log_group()
        if log_id:
            user = await event.get_sender()
            user_name = user.first_name if user else "مستخدم مجهول"
            text = f"**📥 رسـالة جـديدة فـي الـخاص :**\n**👤 مـن:** {user_name}\n**🆔 الآيـدي:** `{event.sender_id}`\n**💬 الـرسالة:**\n{event.text}"
            await client.send_message(log_id, text)
