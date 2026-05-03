import asyncio
from telethon import events
from __main__ import client

# الإعدادات
approved_users = set()
warnings = {}
MAX_WARNINGS = 4

# النص العريض والسادة كما طلبت
PM_TEXT = """**- مرحباً بك في خاص المتمرد 🦅**
**- أنا نظام الحماية التلقائي تم تطويري من قبل المتمرد.**

**- المطور مشغول حالياً، يرجى اختيار سبب تواصلك.**
**⚠️ تحذير: لديك {warns}/{max_warns} محاولات.**
**- إذا تجاوزت الحد سيتم حظرك تلقائياً.**"""

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_permit_system(event):
    sender = await event.get_sender()
    if not sender or sender.bot or event.sender_id in approved_users:
        return
    
    if event.sender_id == (await client.get_me()).id:
        return

    user_id = event.sender_id
    if user_id not in warnings:
        warnings[user_id] = 0
    
    warnings[user_id] += 1
    
    # حظر تلقائي إذا تجاوز المحاولات
    if warnings[user_id] > MAX_WARNINGS:
        await event.reply("**- تم تجاوز الحد المسموح.. وداعاً (حظر) 🚫**")
        from telethon.tl.functions.contacts import BlockRequest
        await client(BlockRequest(id=user_id))
        return

    # إرسال التحذير
    current_warns = warnings[user_id]
    await event.reply(PM_TEXT.format(warns=current_warns, max_warns=MAX_WARNINGS))

print("✅ نظام حماية المتمرد (بدون أزرار) جاهز للعمل!")
