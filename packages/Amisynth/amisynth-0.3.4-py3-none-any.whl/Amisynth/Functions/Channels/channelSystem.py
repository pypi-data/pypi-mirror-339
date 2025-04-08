import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def channelSystem(*args, **kwargs):
    if "ctx_join_member_env" in kwargs:
        n = kwargs["ctx_join_member_env"].guild.system_channel
        return n
    return ""
