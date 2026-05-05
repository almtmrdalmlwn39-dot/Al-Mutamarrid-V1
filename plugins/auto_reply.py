import asyncio
from telethon import events, functions
from telethon.tl.functions.photos import GetUserPhotosRequest
import main

client = main.client

# قاموس لتتبع المحاولات
SECURITY_DB = {}

# الهوية السيبرانية 
MY_IDENTITY = "📡 نحنُ حـماية الـخصوصية فـي زمـن الاخـتراق العالمي 🛡️"

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def security_system_final_v2(event):
    if not event.out:
        user_id = event.sender_id
        
        # جلب معلومات المرسل (الاسم)
        sender = await event.get_sender()
        first_name = sender.first_name or "يا طيب"
        
        # تتبع العداد
        if user_id not in SECURITY_DB:
            SECURITY_DB[user_id] = 1
        else:
            SECURITY_DB[user_id] += 1
        
        count = SECURITY_DB[user_id]

        # إظهار حالة "يرسل صورة" في الرد الأول و "يكتب" في البقية
        action_type = 'img' if count == 1 else 'typing'
        
        async with client.action(event.chat_id, action_type):
            await asyncio.sleep(1.5)

            # 1. الرد الأول: فخم وجذاب مع صورة بروفايلك
            if count == 1:
                me = await client.get_me()
                photos = await client(GetUserPhotosRequest(user_id=me.id, offset=0, max_id=0, limit=1))
                
                text = (
                    "**🌹 أهـلاً بـك فـي رحـاب الـمتمرد الـتقني.**\n"
                    "━━━━━━━━━━━━━━\n"
                    "**نـقدر تـواصلك الـراقي، وتـأكد أن رسـالتك مـحل اهـتمامنا.**\n"
                    "**سـيتم الـرد علـيك في اقرب وقت ممكن ان تـفرغ الـمطور مـن تـأمين الأنـظمة.**\n"
                    "━━━━━━━━━━━━━━\n"
                    f"**{MY_IDENTITY}**"
                )
                
                if photos.photos:
                    await event.reply(text, file=photos.photos[0])
                else:
                    await event.reply(text)

            # 2. من المحاولة 2 إلى 4: تحذير بالاسم (شفاف وفخم)
            elif 2 <= count <= 4:
                rem = 5 - count
                # جعل الاسم بصيغة مائلة (شفافة تقنياً) لإثارة الريبة
                await event.reply(
                    f"**⚠️ تـنبيه مـن نـظام الـحماية الـتلقائي:**\n\n"
                    f"**عـذراً __{first_name}__ ، يـرجى عـدم تـكرار الإرسـال لـضمان اسـتقرار الـتشفير.**\n"
                    f"**مـتبقي لـك ({rem}) مـحاولات قـبل تـفعيل الـحظر الـتلقائي.**\n\n"
                    "**شـكراً لـتعاونك مـع مـمعاييرنا الأمـنية. 🔒**"
                )

            # 3. المحاولة 5: الحظر الفخم (بدون حذف)
            elif count == 5:
                await event.reply(
                    f"**🚫 تـم تـفعيل بـروتوكول الـحظر الـتلقائي يا __{first_name}__ !**\n\n"
                    "**لـلأسف، تـم تـجاوز حـدود الـوصول الـمسموحة.**\n"
                    "**تـم تـقييد حـسابك مـن مـراسلتنا حـالياً لـحماية الخـخصوصية.**\n\n"
                    "**نـلتقي فـي فـضاءٍ أكـثر أماناً. 📡**"
                )
                await asyncio.sleep(1)
                await client(functions.contacts.BlockRequest(id=user_id))
