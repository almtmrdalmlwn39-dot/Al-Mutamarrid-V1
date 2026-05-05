import random
from telethon import events

# استدعاء الكلاينت مباشرة من الملف الرئيسي
from main import client 

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

def is_female(name):
    if not name: return False
    female_hints = ['ة', 'بنت', 'ام ']
    return any(hint in name for hint in female_hints)

# تعديل النمط ليكون مرناً ويستجيب فوراً
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(زبج|قصف)$"))
async def smart_reply(event):
    if event.is_reply:
        try:
            reply = await event.get_reply_message()
            user = await reply.get_sender()
            full_name = (user.first_name or "") if user else ""
            
            msg = random.choice(GIRL_REPLIES if is_female(full_name) else BOY_REPLIES)
            await event.delete()
            await reply.reply(f"**{msg}**")
        except:
            await event.edit(f"**{random.choice(BOY_REPLIES)}**")
    else:
        await event.edit(f"**{random.choice(BOY_REPLIES + GIRL_REPLIES)}**")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.اوامر الزبج$"))
async def show_help(event):
    await event.edit("🦅 **أوامر الزبج:**\n- `.زبج` (بالرد)\n- `.قصف` (بالرد)\n- `.اوامر الزبج`")
