import random
from telethon import events
import main

client = main.client

# --- مخزن الردود ---
# ردود للشباب (قوية ومباشرة)
BOY_REPLIES = [
    "يا خبير بطل هبالة وهرج كلام يدخل الراس.",
    "يا صاحبي أنت محتاج إعادة ضبط مصنع لعقلك.",
    "اسمعني، لو الذكاء بفلوس كنت أنت شحات.",
    "يا منعاه خف علينا، العالم ما يتحملش إبداعك.",
    "شكلك شربت شاي حارق اليوم، هدي اللعب."
]

# ردود للبنات (قصف جبهات بأسلوب أنثوي)
GIRL_REPLIES = [
    "يا خبيرة وفري كلامك، الموضة هذه قديمة.",
    "يا أختي لو الكلام عليه جمرك كنتِ مديونة.",
    "شكلك ضيعتي الطريق، ارجعي لليوزرك أحسن.",
    "بلاش حركات، العقل في راحة وأنتِ متعبة نفسك.",
    "واصلِ، مخزون الضحك عندي محتاج نكتة جديدة."
]

# دالة ذكية لتخمين الجنس من الاسم
def is_female(name):
    female_hints = ['ة', 'بنت', 'ام ', 'نورة', 'سارة', 'ريم', 'امل', 'ليلى']
    return any(hint in name for hint in female_hints)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.(زبج|قصف)"))
async def smart_reply(event):
    reply_msg = ""
    
    if event.is_reply:
        # جلب معلومات الشخص المردود عليه
        reply = await event.get_reply_message()
        user = await client.get_entity(reply.sender_id)
        full_name = (user.first_name or "") + (user.last_name or "")
        
        # فحص إذا كان الاسم يوحي بأنها بنت
        if is_female(full_name):
            reply_msg = random.choice(GIRL_REPLIES)
        else:
            reply_msg = random.choice(BOY_REPLIES)
            
        await event.delete()
        await event.respond(reply_msg, reply_to=event.reply_to_msg_id)
    else:
        # إذا كتبت الأمر بدون رد، يختار رد عام
        reply_msg = random.choice(BOY_REPLIES + GIRL_REPLIES)
        await event.edit(reply_msg)
