import random
from telethon import events
import google.generativeai as genai
from main import client, CMD_HELP

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "قسم الردود الذكية": ["زبج", "قصف"]
})

# وظيفة توليد الرد عبر الذكاء الاصطناعي
async def generate_smart_reply(user_text, reply_type):
    try:
        # صياغة الطلب للذكاء الاصطناعي ليكون الرد بشرياً وقاسياً
        prompt = (
            f"رد على هذه الرسالة: '{user_text}' بأسلوب {reply_type} ساخر جداً وقوي. "
            f"اجعل الرد يبدو كأن شخصاً حقيقياً يكتبه، لا تذكر أي أسماء، "
            f"استخدم لهجة بيضاء أو يمنية خفيفة، واجعل الرد قصيراً ومفحماً."
        )
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except:
        # رد احتياطي في حال فشل الاتصال بالذكاء الاصطناعي
        return "كلامك هذا يحتاج إعادة ضبط مصنع، ركز قبل ما تتكلم."

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(زبج|قصف)$"))
async def ai_reply_cmd(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يجب الرد على رسالة الشخص ليتم تحليلها والرد عليها!**")
    
    await event.edit("**🔄 جـاري تـحـلـيـل الـكلام والـقـصف...**")
    
    try:
        reply_msg = await event.get_reply_message()
        user_text = reply_msg.text or "صورة أو ملصق"
        reply_type = "قصف جبهات" if ".قصف" in event.text else "زبج وسخرية"
        
        # توليد الرد الذكي
        final_reply = await generate_smart_reply(user_text, reply_type)
        
        await event.delete()
        await reply_msg.reply(f"**{final_reply}**")
        
    except Exception as e:
        await event.edit(f"**⚠️ عذراً، حدث خطأ في معالجة الرد الذكي.**")
