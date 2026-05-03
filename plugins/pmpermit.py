import asyncio
from telethon import events, Button
from telethon.tl.functions.contacts import BlockRequest

approved_users = []
warnings = {}
MAX_WARNINGS = 4

# النص عريض وسادة كما طلبت
PM_TEXT = """
**- مرحبا بك في خاص المتمرد 🦅**
**- انا نظام الحماية التلقائي تم تطويري من قبل المتمرد.**

**- المطور مشغول حاليا، يرجى اختيار سبب  تواصلك.**
**⚠️ تحذير: لديك ({warns}/{max_warns}) محاولات.**
**اذا تجاوزت الحد سيتم حظرك تلقائيا.**
"""

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_permit_system(event):
    sender = await event.get_sender()
    if not sender or sender.bot or event.sender_id == OWNER_ID:
        return
    
    user_id = event.sender_id
    if user_id in approved_users:
        return
        
    if user_id not in warnings:
        warnings[user_id] = 1
    else:
        warnings[user_id] += 1
        
    if warnings[user_id] > MAX_WARNINGS:
        await event.reply("**- تم تجاوز حد الرسائل المسموح به 🚫.**\n**- تم حظرك تلقائيا من قبل النظام.**")
        await bot(BlockRequest(id=user_id))
        return

    # جلب صورة بروفايلك الحالية وارسالها
    # البوت سيقوم بتحميل صورة بروفايلك وارسالها كخلفية للرد
    my_photo = await bot.download_profile_photo(OWNER_ID)

    # الازرار الشفافة
    buttons = [
        [Button.inline("طلب سورس", data="re_src"), Button.inline("تواصل شخصي", data="re_prm")],
        [Button.inline("استفسار تقني", data="re_tech")]
    ]
    
    warn_msg = PM_TEXT.format(warns=warnings[user_id], max_warns=MAX_WARNINGS)
    await event.reply(warn_msg, file=my_photo, buttons=buttons)

@bot.on(events.NewMessage(pattern=r"\.سماح", outgoing=True))
async def allow(event):
    user_id = event.chat_id
    if user_id not in approved_users:
        approved_users.append(user_id)
    if user_id in warnings:
        del warnings[user_id]
    await event.edit("**- تم السماح للمستخدم بالمراسلة ☑️.**")

@bot.on(events.NewMessage(pattern=r"\.رفض", outgoing=True))
async def deny(event):
    user_id = event.chat_id
    await event.edit("**- تم حظر المستخدم 🚫.**")
    await bot(BlockRequest(id=user_id))
