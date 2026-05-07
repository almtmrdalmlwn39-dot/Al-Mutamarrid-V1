from telethon import events, functions, errors
import asyncio

@client.on(events.NewMessage(outgoing=True, pattern=r"\.سحب (.*)"))
async def scrap_members(event):
    target = event.pattern_match.group(1).strip()
    if not target:
        return await event.edit("**⚠️ حدد معرف القروب**")
    
    await event.edit("**🛡️ جاري السحب..**")
    try:
        source_chat = await client.get_entity(target)
        users_list = await client.get_participants(source_chat, limit=100)
        
        count = 0
        for user in users_list:
            if user.bot or user.deleted: continue
            try:
                await client(functions.channels.InviteToChannelRequest(event.chat_id, [user.id]))
                count += 1
                await asyncio.sleep(2) 
            except: continue
        
        await event.respond(f"**✅ تم سحب {count} عضو بنجاح.**")
    except Exception as e:
        await event.edit(f"**❌ خطأ: {str(e)}**")
