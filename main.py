@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_super_menu(event):
    if not CMD_HELP:
        return await event.edit("**⚠️ القائمة فارغة.. تأكد من تعريف الحزم في المجلدات.**")
        
    # واجهة القائمة بستايل زدثون الفخم
    msg = "ᯓ **𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - قائمــة الاوامــر العامــه** 𓆪\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    msg += "⌔ **مـرحبـاً عـزيـزي لـ الـمتمـرد الـتقنـي**\n"
    msg += "⌔  **اضغـط ع الامـر لـ النسـخ**\n"
    msg += "⌔ **لا تنسى وضـع نقطه (.) بداية كل امـر :**\n\n"

    # جلب أسماء الحزم وترتيبها
    plugins = sorted(CMD_HELP.keys())
    
    for i, plugin in enumerate(plugins, 1):
        # التنسيق الرقمي لزدثون
        msg += f" **.م{i}** ➪ **اوامــر {plugin}**\n"

    msg += "\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    msg += f"\n  ـ **SOURCE ALMTMRD - {datetime.now().year}**"
    
    await event.edit(msg)

# دالة ذكية لفتح الحزم (عند كتابة .م1، .م2 الخ)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.م(\d+)"))
async def open_rebel_package(event):
    index = int(event.pattern_match.group(1)) - 1
    plugins = sorted(CMD_HELP.keys())
    
    if 0 <= index < len(plugins):
        plugin_name = plugins[index]
        cmds = CMD_HELP[plugin_name]
        
        res = f"ᯓ **اوامــر {plugin_name}** 𓆪\n"
        res += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
        res += "⌔ **اضغـط ع الامـر لـ النسـخ :**\n\n"
        
        # عرض الأوامر بشكل مصفوفة أنيقة
        for cmd in cmds:
            res += f"`.{cmd}`  "
            
        res += "\n\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
        await event.edit(res)
