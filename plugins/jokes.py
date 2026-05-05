import random # تم تصحيح حرف الـ i إلى صغير ليعمل الكود
from telethon import events
import main

client = main.client

# --- مخزن الردود ---
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

# دالة تخمين الجنس
def is_female(name):
    if not name: return False
    female_hints = ['ة', 'بنت', 'ام ']
    return any(hint in name for hint in female_hints)

# --- كود القصف والزبج ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(زبج|قصف)$"))
async def smart_reply(event):
    if event.is_reply:
        try:
            reply = await event.get_reply_message()
            user = await reply.get_sender()
            full_name = (user.first_name or "") if user else ""
            
            if is_female(full_name):
                reply_msg = random.choice(GIRL_REPLIES)
            else:
                reply_msg = random.choice(BOY_REPLIES)
                
            await event.delete()
            await reply.reply(f"**{reply_msg}**")
        except:
            await event.edit(f"**{random.choice(BOY_REPLIES)}**")
    else:
        # إذا جربت في الحافظة بدون رد
        reply_msg = random.choice(BOY_REPLIES + GIRL_REPLIES)
        await event.edit(f"**{reply_msg}**")

# --- كود عرض الأوامر (إضافة جديدة) ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.اوامر الزبج$"))
async def show_zabj_help(event):
    help_text = """
🦅 **أوامر الزبج للمتمرد التقني:**
- `.زبج` : بالرد على شخص (يقصف جبهته).
- `.قصف` : نفس عمل زبج.
- `.اوامر الزبج` : لعرض هذه القائمة.

💡 *ملاحظة: السورس يفرق بين الولد والبنت تلقائياً.*
    """
    await event.edit(help_text)
