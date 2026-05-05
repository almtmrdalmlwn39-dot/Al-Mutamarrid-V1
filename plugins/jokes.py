import random
from telethon import events
import main

client = main.client

# --- مخزن الردود (نفس حقك بالضبط) ---
BOY_REPLIES = [
    "يا خبير بطل هبالة وهرج كلام يدخل الراس.",
    "يا صاحبي أنت محتاج إعادة ضبط مصنع لعقلك.",
    "اسمعني، لو الذكاء بفلوس كنت أنت شحات.",
    "يا منعاه خف علينا، العالم ما يتحملش إبداعك.",
    "شكلك شربت شاي حارق اليوم، هدي اللعب."
]

GIRL_REPLIES = [
    "يا خبيرة وفري كلامك، الموضة هذه قديمة.",
    "يا أختي لو الكلام عليه جمرك كنتِ مديونة.",
    "شكلك ضيعتي الطريق، ارجعي لليوزرك أحسن.",
    "بلاش حركات، العقل في راحة وأنتِ متعبة نفسك.",
    "واصلِ، مخزون الضحك عندي محتاج نكتة جديدة."
]

# دالة تخمين الجنس (نفس حقك)
def is_female(name):
    if not name: return False
    female_hints = ['ة', 'بنت', 'ام '] # شلنا الأسماء المحددة وخلينا التاء المربوطة والكلمات العامة
    return any(hint in name for hint in female_hints)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.(زبج|قصف)"))
async def smart_reply(event):
    reply_msg = ""
    
    if event.is_reply:
        # 1. جلب الرسالة المردود عليها
        reply = await event.get_reply_message()
        
        # 2. التعديل الجوهري هنا (بدل get_entity نستخدم get_sender)
        # هذا السطر أسرع وما يعلق الكود
        user = await reply.get_sender()
        
        full_name = (user.first_name or "") if user else ""
        
        # 3. فحص الجنس واختيار الرد
        if is_female(full_name):
            reply_msg = random.choice(GIRL_REPLIES)
        else:
            reply_msg = random.choice(BOY_REPLIES)
            
        await event.delete()
        # 4. الرد المباشر (Reply) ليكون القصف دقيق
        await reply.reply(f"**{reply_msg}**")
    else:
        # إذا كتبت الأمر في الحافظة بدون "رد"
        reply_msg = random.choice(BOY_REPLIES + GIRL_REPLIES)
        await event.edit(f"**{reply_msg}**")
