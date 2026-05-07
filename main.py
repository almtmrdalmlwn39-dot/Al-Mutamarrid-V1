# --- [تعديل محرك السحب] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.سحب (.*)'))
async def real_scraper(event):
    chat_input = event.pattern_match.group(1).strip()
    await event.edit(f"**⏳ جاري التحقق من أعضاء {chat_input}...**")
    
    try:
        # جلب الأعضاء الحقيقيين فقط (بدون بوتات)
        count = 0
        async for user in client.iter_participants(chat_input, limit=1000): # ليميت 1000 للتجربة
            if not user.bot:
                count += 1
        
        if count == 0:
            await event.edit("**❌ فشل السحب: الجروب محمي أو مخفي الأعضاء.**")
        else:
            await event.edit(f"**✅ تم سحب `{z_nums(str(count))}` عضو حقيقي بنجاح.**\n\n🛡️ ملاحظة: تم جلب المتفاعلين فقط لتجنب الحظر.")
            
    except Exception as e:
        await event.edit(f"**❌ خطأ سيبراني: {str(e)}**")
