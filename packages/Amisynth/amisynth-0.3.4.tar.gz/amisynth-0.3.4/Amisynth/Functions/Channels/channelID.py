import xfox
import discord
import Amisynth.utils as utils
@xfox.addfunc(xfox.funcs)
async def channelID(nombre: str = None, *args, **kwargs):
    context = utils.ContextAmisynth()
    if nombre is None:
        channel  = context.channel_id
    else:
        channel = context.get_channel_id_by_name(nombre)

    return channel
