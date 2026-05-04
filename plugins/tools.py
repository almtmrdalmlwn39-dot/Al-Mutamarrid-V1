import os
import asyncio
from telethon import events
from __main__ import client  # استدعاء العميل من الملف الرئيسي

# --- أمر سحب الميديا المقيدة ---
@client.on(events.NewMessage(pattern=r"^\.سحب$", outgoing=True))
async def steal(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يـا مـتمرد، يـجب الـرد عـلى الـرسالة أولاً!**")
    
    reply = await event.get_reply_message()
    if not reply.media:
        return await event.edit("**⚠️ هـذه الـرسالة لا تـحتوي عـلى مـيديا (صورة/فيديو)!**")
    
    await event.edit("**🚀 جـاري اخـتراق الـقيد وسـحب الـمحتوى...**")
    
    try:
        # تحميل الميديا حتى لو كانت مقيدة
        path = await reply.download_media()
        
        # إرسال المحتوى للرسائل المحفوظة (me)
        await client.send_file(
            "me", 
            path, 
            caption="**✅ تـم سـحب الـمحتوى بـنجاح بـواسطة الـمتمرد 🦅\n- نـحنُ نـصنعُ الـفرق حـيثُ يـعجزُ الآخرون.**"
        )
        
        await event.edit("**✅ تـم الـسحب بـنجاح! راجـع رسـائلك الـمحفوظة.**")
        
        # تنظيف الملفات المؤقتة
        if os.path.exists(path):
            os.remove(path)
            
    except Exception as e:
        await event.edit(f"**❌ حـدث خـطأ فـي الـسحب: `{str(e)}`**")

# --- أمر الفحص السريع ---
@client.on(events.NewMessage(pattern=r"^\.فحص_السحب$", outgoing=True))
async def check_steal(event):
    await event.edit("**🛡️ مـحرك الـسحب شـغال بـكفاءة عـالية يـا مـتمرد!**")
